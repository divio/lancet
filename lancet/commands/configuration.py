import configparser
import os

import click

import keyring

from ..settings import PROJECT_CONFIG, USER_CONFIG
from ..utils import taskstatus


@click.command()
@click.option(
    "-f", "--force/--no-force",
    default=False,
    help="Setup even if .lancet already exists.",
)
@click.option(
    "-d", "--debug/--no-debug",
    default=False,
    help="Adds additional steps to the wizard for debugging.",
)
@click.pass_context
def setup(ctx, force, debug):
    """Wizard to create the user-level configuration file."""
    if os.path.exists(USER_CONFIG) and not force:
        click.secho(
            f'An existing configuration file was found at "{USER_CONFIG}"',
            fg="red",
            bold=True,
        )
        click.secho(
            "Please remove it before in order to run the setup wizard or use"
            "the\n --force flag to overwrite it."
        )
        ctx.exit(1)

    current_step = 1
    total_steps = 3
    if debug:
        total_steps += 1

    # configure gitlab
    click.secho(f"Step {current_step} of {total_steps}")
    click.secho("Enter your Gitlab username:")
    gitlab_user = click.prompt("Username")
    click.secho()
    current_step += 1

    # configure harvest
    click.secho(f"Step {current_step} of {total_steps}")
    click.secho(
        "Add the company wide account ID. \n"
        "You can get it from https://id.getharvest.com/developers."
    )
    timer_id = click.prompt("Accound ID")
    click.secho()
    current_step += 1

    click.secho(f"Step {current_step} of {total_steps}")
    click.secho(
        "Add the user ID found on your profile's URL: \n"
        "https://divio.harvestapp.com/people/{YOUR_ID}/."
    )
    timer_user = click.prompt("User ID")
    click.secho()
    current_step += 1

    if debug:
        click.secho(
            "Running with --debug, additional setup parameters will "
            "be requested.",
            fg="green",
            bold=True,
        )
        click.secho(f"Step {current_step} of {total_steps}")
        click.secho("Please provide the SENTRY_DSN link:")
        sentry_dsn = click.prompt("Sentry DSN")
        click.secho()
        current_step += 1

    # writing configuration
    config = configparser.ConfigParser()

    config.add_section("lancet")
    config.add_section("tracker:gitlab")
    config.add_section("scm-manager:gitlab")
    config.add_section("timer:harvest")

    if debug and sentry_dsn:
        config.set("lancet", "sentry_dsn", sentry_dsn)
    config.set("tracker:gitlab", "username", gitlab_user)
    config.set("scm-manager:gitlab", "username", gitlab_user)
    config.set("timer:harvest", "username", timer_id)
    config.set("timer:harvest", "user_id", timer_user)

    with open(USER_CONFIG, "w") as fh:
        config.write(fh)

    click.secho(
        f'Configuration correctly written to "{USER_CONFIG}".',
        fg="green",
    )


@click.command()
@click.option(
    "-f",
    "--force/--no-force",
    default=False,
    help="Init even if .lancet already exists.",
)
@click.pass_context
def init(ctx, force):
    """Wizard to create a project-level configuration file."""
    if os.path.exists(PROJECT_CONFIG) and not force:
        click.secho(
            'An existing configuration file was found at "{}".\n'.format(
                PROJECT_CONFIG
            ),
            fg="red",
            bold=True,
        )
        click.secho(
            "Please remove it before in order to run the setup wizard or use\n"
            "the --force flag to overwrite it."
        )
        ctx.exit(1)

    project_id = click.prompt("Project id on Gitlab")
    project_group = click.prompt("Project group on Gitlab")
    base_branch = click.prompt("Integration branch", default="master")

    virtualenvs = (".venv", ".env", "venv", "env")
    for p in virtualenvs:
        if os.path.exists(os.path.join(p, "bin", "activate")):
            venv = p
            break
    else:
        venv = ""
    venv_path = click.prompt("Path to virtual environment", default=venv)

    project_id = click.prompt("Project ID on Harvest", type=int)
    task_id = click.prompt("Task ID on Harvest", type=int)

    config = configparser.ConfigParser()

    config.add_section("lancet")
    config.set("lancet", "virtualenv", venv_path)

    config.add_section("tracker")
    config.set("tracker", "project_id", project_id)
    config.set("tracker", "group_id", project_group)
    config.set("tracker", "active_status", "dev::doing")
    config.set("tracker", "paused_status", "")
    config.set("tracker", "review_status", "dev::review")
    config.set("tracker", "testing_status", "dev::testing")
    config.set("tracker", "deploy_status", "rollout::to be deployed")
    config.set("tracker", "done_status", "step::rollout")

    config.add_section("harvest")
    config.set("harvest", "project_id", str(project_id))
    config.set("harvest", "task_id", str(task_id))

    config.add_section("repository")
    config.set("repository", "base_branch", base_branch)

    with open(PROJECT_CONFIG, "w") as fh:
        config.write(fh)

    click.secho(
        '\nConfiguration correctly written to "{}".'.format(PROJECT_CONFIG),
        fg="green",
    )


@click.command()
@click.argument("service", required=False)
@click.pass_obj
def logout(lancet, service):
    """Forget saved passwords for the web services."""
    if service:
        services = [service]
    else:
        services = ["tracker", "harvest"]

    for service in services:
        url = lancet.config.get(service, "url")
        key = "lancet+{}".format(url)
        username = lancet.config.get(service, "username")
        with taskstatus("Logging out from {}", url) as ts:
            if keyring.get_password(key, username):
                keyring.delete_password(key, username)
                ts.ok("Logged out from {}", url)
            else:
                ts.ok("Already logged out from {}", url)


@click.command()
@click.pass_obj
def _services(lancet):
    """List all currently configured services."""

    def get_services(config):
        for s in config.sections():
            if config.has_option(s, "url"):
                if config.has_option(s, "username"):
                    yield s

    for s in get_services(lancet.config):
        click.echo("{}[Logout from {}]".format(s, lancet.config.get(s, "url")))
