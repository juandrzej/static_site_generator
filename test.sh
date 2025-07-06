#!/bin/bash
# This tells Python where to look for modules
export PYTHONPATH=src
# This command tells Python to use the standard library's unittest module to run all the tests (discover) it can find in the tests directory.
python3 -m unittest discover -s tests/
