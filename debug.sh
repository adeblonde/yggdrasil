#!/bin/bash

### activate test virtualenv
# ../testenv/bin/activate

source ../user_setenv.sh

### recompile and reinstall package
# pip3 install -e .

### execute yggdrasil
ygg --configfile yggdrasil/test/test_config.yml --workfolder ../work/
