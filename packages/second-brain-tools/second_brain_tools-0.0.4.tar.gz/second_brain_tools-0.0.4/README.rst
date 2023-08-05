2023
====

I am releasing a hotfix for the PyPI package, version 0.0.4. This update addresses a minor issue caused by a change in the naming scheme of GitHub repositories, which was preventing the package from building properly in all Python environments. Additionally, I would like to inform you that support for pypy37 has been discontinued.

I am currently addressing the challenges caused by the insufficient documentation and actively working on improving it.

EOL
===

The project has been flagged as EOL (End of Life) on December 2022. Moving forward to a more simplistic approach for better automation and other changes. You can still use the structure but please don't expect more updates or support.

Overview
========

[![GitHub Actions Build Status](https://github.com/rohanbatrain/Second-Brain-Tools/actions/workflows/pylint.yml/badge.svg)](https://github.com/rohanbatrain/Second-Brain-Tools/actions/)
[![GitHub Actions Build Status](https://github.com/rohanbatrain/Second-Brain-Tools/actions/workflows/build.yml/badge.svg)](https://github.com/rohanbatrain/Second-Brain-Tools/actions/)
[![GitHub Actions Build Status](https://github.com/rohanbatrain/Second-Brain-Tools/actions/workflows/mkdocs.yml/badge.svg)](https://github.com/rohanbatrain/Second-Brain-Tools/actions/)
[![Coverage Status](https://codecov.io/gh/rohanbatrain/Second-Brain-Tools/branch/main/graphs/badge.svg?branch=main)](https://codecov.io/github/rohanbatrain/Second-Brain-Tools)
[![PyPI Package latest release](https://img.shields.io/pypi/v/second-brain-tools.svg)](https://pypi.org/project/second-brain-tools)
[![PyPI Wheel](https://img.shields.io/pypi/wheel/second-brain-tools.svg)](https://pypi.org/project/second-brain-tools)
[![Supported versions](https://img.shields.io/pypi/pyversions/second-brain-tools.svg)](https://pypi.org/project/second-brain-tools)
[![Supported implementations](https://img.shields.io/pypi/implementation/second-brain-tools.svg)](https://pypi.org/project/second-brain-tools)
[![Commits since latest release](https://img.shields.io/github/commits-since/rohanbatrain/Second-Brain-Tools/v0.0.4.svg)](https://github.com/rohanbatrain/Second-Brain-Tools/compare/v0.0.4...main)

This project is a toolset for Second Brain. It helps to quickly and efficiently create notes using Second Brain Vault.

- Free software: Apache Software License 2.0

Prerequisites
=============

1. Make sure you have Python 3 and pip installed.
2. Please install Git on your specific system in order to run this code.

Installation
============

::

    pip install https://github.com/rohanbatrain/Second-Brain-Tools/archive/main.zip

Documentation
=============

To use the project:

.. code-block:: python

    from second_brain_tools import cli  
    cli.main()

Or from your terminal:

.. code-block:: bash

    second-brain-tools --help
