#!/bin/bash

### run tests 
# python3 setup.py test

### python unit tests
nosetests

### activate test virtualenv
# ../testenv/bin/activate

### recompile and reinstall package
pip3 install -e .