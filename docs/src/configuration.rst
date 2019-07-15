=============
Configuration
=============


Global and local configuration
------------------------------

Lancet gathers data from two different settings file:

* A global ``.lancet`` file from your user path (e.g. ~/.lancet)
* A project specific ``.lancet`` file from your projects root directory


Global setup
============

Lancet requires a user-level file to identify your account settings such as
for Gitlab, Harvest, Sentry and others.

The ``lancet setup`` command runs you through the setup step by step and
generates the ``~/.lancet`` file automatically for your depending on the
data provided, here an example::

    [lancet]
    sentry_dsn = {sentry_dsn_link}

    [tracker:gitlab]
    username = {gitlab_username}

    [scm-manager:gitlab]
    username = {gitlab_username}

    [timer:harvest]
    username = {harvest_id}
    user_id = {harvest_user_id}

This file gets stored into your user directory ``~/.lancet``.


Project setup
=============

In addition lancet requires a ``.lancet`` file that resides in your projects
root folder.

The ``lancet init`` command runs you through the setup step by step and
generates the ``project_path/.lancet`` file automatically for your depending on the
data provided, here an example::

    TODO: needs to be adaoted / simplified
    [tracker]
    project_id = {gitlab_project_id}
    group_id = {gitlab_group_id}
    paused_status =
    active_status = doing
    review_status = review

    [timer]
    project_id = {harvest_project_id}
    task_id = {harvest_task_id}


Project initialization
======================


Configuration directives reference
==================================
