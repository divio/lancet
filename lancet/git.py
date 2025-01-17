import re
import sys

import click

import pygit2
import six
from giturlparse import parse as giturlparse
from slugify import slugify

from .utils import taskstatus


TOKEN_USER = b"x-oauth-basic"


class PrefixedIDBranchName:
    slug_length = 50

    def get_prefix(self, issue):
        raise NotImplementedError()

    def get_issue_key(self, branch_name):
        raise Exception("Unable to find current issue.")

    def __call__(self, issue):
        discriminator = "{}{}_".format(self.get_prefix(issue), issue.id)
        slug = slugify(issue.summary[: self.slug_length])
        full_name = "{}{}".format(discriminator, slug)
        return discriminator, full_name


class FixedPrefixIDBranchName(PrefixedIDBranchName):
    def __init__(self, prefix):
        self._prefix = prefix

    def get_prefix(self, issue):
        return self._prefix

    def get_issue_key(self, branch_name):
        match = re.search(self._prefix + r"([A-Z]{2,}-[0-9]+)", branch_name)
        if match is None:
            raise Exception("Unable to find current issue.")
        return match.group(1)


class CredentialsCallbacks(pygit2.RemoteCallbacks):
    def credentials(self, url, username_from_url, allowed_types):
        if allowed_types & pygit2.credentials.GIT_CREDTYPE_USERNAME:
            raise NotImplementedError
        elif allowed_types & pygit2.credentials.GIT_CREDTYPE_SSH_KEY:
            return pygit2.KeypairFromAgent(username_from_url)
        else:
            return None


class TaskTypePrefixIDBranchName(PrefixedIDBranchName):
    def __init__(self, prefixes):
        self._prefixes = prefixes

    def get_prefix(self, issue):
        try:
            return self._prefixes[str(issue.type)]
        except KeyError:
            pass

        try:
            return self._prefixes[None]
        except KeyError:
            pass

        raise ValueError(
            'Could not find a prefix for issue type "{}"'.format(
                issue.fields.issuetype
            )
        )

    def get_issue_key(self, branch_name):
        for prefix in six.itervalues(self._prefixes):
            match = re.search(prefix + r"((?:[A-Z]{2,}-)?[0-9]+)", branch_name)
            if match is not None:
                return match.group(1)
        else:
            raise Exception("Unable to find current issue.")

    @classmethod
    def fromstring(cls, string):
        prefixes = string.split(",")
        prefixes = (p.split(":") for p in prefixes)
        prefixes = ((None, p[0]) if len(p) == 1 else p for p in prefixes)
        prefixes = dict(prefixes)
        return cls(prefixes)


def prefixed_id_branch_name(lancet):
    prefix = lancet.config.get("repository", "branch_name_prefix")
    return TaskTypePrefixIDBranchName.fromstring(prefix)


class BranchGetter:
    def __init__(self, base_branch, branch_name_getter, remote_name="origin"):
        self.base_branch = base_branch
        self.remote_name = remote_name
        self.get_branch_name = branch_name_getter

    def get_base_branch(self, repo):
        return repo.lookup_branch(
            "{}/{}".format(self.remote_name, self.base_branch),
            pygit2.GIT_BRANCH_REMOTE,
        )

    def get_branch(self, repo, issue, from_remote=False):
        discriminator, full_name = self.get_branch_name(issue)

        if from_remote:
            branch_type = pygit2.GIT_BRANCH_REMOTE
            discriminator = "{}/{}".format(self.remote_name, discriminator)
        else:
            branch_type = pygit2.GIT_BRANCH_LOCAL

        branches = [
            b
            for b in repo.listall_branches(branch_type)
            if b.startswith(discriminator)
        ]

        if len(branches) > 1:
            click.secho(
                "Multiple matching branches found!", fg="red", bold=True
            )
            click.echo()
            click.echo(
                "The prefix {} matched the following branches:".format(
                    discriminator
                )
            )
            click.echo()
            for b in branches:
                click.echo(" {} {}".format(click.style("*", fg="red"), b))
            click.echo()
            click.echo("Please remove all but one in order to continue.")
            sys.exit(1)
        elif branches:
            branch = repo.lookup_branch(branches[0], branch_type)
            if from_remote:
                branch = repo.create_branch(full_name, branch.get_object())
            elif branch.branch_name != full_name:
                # We only need to rename if we're working on an already
                # existing local branch
                branch.rename(full_name)
                branch = repo.lookup_branch(full_name)
            return branch

    def __call__(self, repo, issue, create=True):
        branch = self.get_branch(repo, issue)

        if not branch:
            # No local branches found, fetch remote
            with taskstatus('Fetching from "{}"', self.remote_name) as ts:
                remote = repo.lookup_remote(self.remote_name)
                if not remote:
                    ts.abort('Remote "{}" not found', self.remote_name)

                remote.fetch(callbacks=CredentialsCallbacks())
                ts.ok('Fetched latest changes from "{}"', self.remote_name)

            # Check remote branches
            with taskstatus("Creating working branch") as ts:
                branch = self.get_branch(repo, issue, from_remote=True)

                # Create off origin base branch
                if branch:
                    ts.ok(
                        "Created new working branch based on existing "
                        "remote branch"
                    )
                elif create:
                    _, full_name = self.get_branch_name(issue)

                    base = self.get_base_branch(repo)
                    if not base:
                        ts.abort(
                            'Base branch "{}" not found on remote "{}"',
                            self.base_branch,
                            self.remote_name,
                        )
                    branch = repo.create_branch(full_name, base.peel())
                    ts.ok("Created new working branch")

        return branch


class Repository(pygit2.Repository):
    def lookup_remote(self, name):
        return self.remotes[name]

    def get_credentials_for_remote(self, remote):
        if not remote:
            return
        p = giturlparse(remote.url)
        remote_username = p.user

        if p.protocol == "ssh":
            credentials = pygit2.KeypairFromAgent(remote_username)
        elif p.protocol == "https":
            raise NotImplementedError("No authentication support.")
            # credentials = pygit2.UserPass(username, password)

        return credentials
