=========
Changelog
=========


0.8.0 - (unreleased)
====================

* Added linting to packages
* Added test framework
* Added formatted documentation
* Aligned code with other addons


0.7.6 (2015-06-11)
==================

* Add a command to list versions
* Update dependencies
* Don't report ``bdb.BdbQuit`` exceptions to Sentry


0.7.5 (2015-06-06)
==================

* Improve the contribution guidelines
* Add Sentry logging for exceptions


0.7.4 (2015-06-04)
==================

* Update requirements
* Add a command to manage release notes
* Improve the contribution guidelines


0.7.3 (2015-05-31)
==================

* Update requirements
* Allow to specify the path to the deployment spec in the settings
* Add some packaging tools to the contrib commmands


0.7.2 (2015-05-13)
==================

* Update to libgit 0.22 (requires updated of the shared library).
* Fixed a bug in the handling of Harvest API errors.
* Make the issue argument to the ``time`` command optional.
* Add support for command aliases.


0.7.1 (2015-02-26)
==================

* Expand users in the template path.
* Update requirements.


0.7.0 (2015-02-26)
==================

* Added support for Jinja2-rendered templates to define the initial
  pull-request title/body used by the ``pr`` command.
* Update the Harvest API to make use of the ``external_ref`` argument instead
  of simulating a browsing session. This trims down on the number of requests
  needed to start a timer and improves performance.
* Added a ``checkout`` command to easily checkout an existing branch based
  solely on the issue ID.
* All commands are now dynamically loaded. Additional commands can be defined
  in the settings (this also supports custom external commands).
* The Harvest project is now retrieved from the supertask if none can be
  defined by looking at the subtask.
* Get the github login token from the keychain in a more robust way.


0.6.0 (2015-01-19)
==================

* Added support for pluggable Harvest task/project mapper.
* Added support for epics based time tracking.
* Added support for pluggable branch naming backends.
* Added support for different branch prefixes based on issue type.
* Added URL hints to ``lancet setup``.
* Fix assignee comparison bug.
* More robust support for flawed versions of the git ``osxkeychain``
  credentials helper.
* Increase the slug length in branch names to 50 chars.
* Built in support for debugging exceptions.


0.5.1 (2015-01-13)
==================

* Coerce config values to int when calling ``init``.


0.5.0 (2015-01-05)
==================

* Include all resources in the distribution.
* Cleanup docker-related leftovers.
* Added a ``pr`` command to automate pull requests creation.
* The ``logout`` command can now logout from a single service.


0.4.2 (2015-01-05)
==================

* Fix ``python-slugify`` requirement.


0.4.1 (2015-01-05)
==================

* Update requirements.


0.4.0 (2015-01-05)
==================

.. warning::

   If your setup includes remote configured to be accessed over SSH, you may
   need to reinstall ``libgit2`` with ``brew reinstall libgit2 --with-libssh2``.

* Added facilities to integrate with the current shell, for stuff like cd'ing
  to other directories or activating virtual environments.
* Added a ``--version`` option to ``lancet``.
* Fetch latest changes from origin before creating new working branches (#1).
* Added an ``activate`` command to ``cd`` to the project directory and
  (optionally) activate a virtual environment.
* Added the ``harvest-projects`` and ``harvest-tasks`` commands to list
  projects/tasks IDs from Harvest.
* Added an ``init`` command to create project-level configuration files (#2).


0.3.0 (2014-12-30)
==================

* Handle unassigned issues (#5).
* Avoid logging out the web user when accessign the JIRA API (#4).
* Initial documentation stub (#3).
