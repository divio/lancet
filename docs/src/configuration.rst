=============
Configuration
=============


Initial setup
=============

Lancet requires a user-level file to identify your account settings such as
for Gitlab, Harvest, Sentry and others.

The ``lancet setup`` command runs you through the setup step by step and
generates the ``.lancet`` file automatically for your depending on the
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


Where does ``lancet`` read the configuration from?
=================================================

Create a ``.lancet`` configuration file inside your projects root. The contents should be::

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
