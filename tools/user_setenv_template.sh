#!/bin/bash

export AUTH_DIR=

export WORK_DIR=

export CODE_DIR=

if [ ! -e $WORK_DIR ]
then
        mkdir -p $WORK_DIR
fi

if [ ! -e $CODE_DIR ]
then
        mkdir -p $CODE_DIR
fi

### set AWS creds file
export AWS_CREDS=credentials.csv

### set yggdrasil's home
export YGG_HOME=x

### ssh key to use for yggdrasil
export SSH_KEY=KEY.pem

### vault password file
export VAULT_PSSWD=vault_pass.txt

### encrypted vault creds
export ENCRYPT_CRED=credentials_encrypted.yml

### set user name
export USER=