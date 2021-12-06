#!/bin/bash
# Run unittests

PYTHONPATH=solutions python3 -m unittest discover "$@"
