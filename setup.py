#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

from lancet import __version__


REQUIREMENTS = [
    "attrs",
    "click",
    "git-url-parse",
    "github3.py",
    "Jinja2",
    "jira",
    "keyring",
    "keyrings.alt",
    "pygit2>=0.28,<0.29",
    "python-gitlab",
    "python-slugify",
    "requests",
    "sentry-sdk",
    "tabulate",
    "uritemplate.py",
]


CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    'Environment :: Web Environment',
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
]


setup(
    name="lancet",
    version=__version__,
    author="Divio AG",
    author_email="info@divio.ch",
    url='https://github.com/divio/lancet',
    license="MIT",
    description="Command line utility to streamline various development activities.",
    long_description=open('README.rst').read(),
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIREMENTS,
    classifiers=CLASSIFIERS,
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    entry_points="""
        [console_scripts]
        lancet = lancet.cli:main
    """,
)
