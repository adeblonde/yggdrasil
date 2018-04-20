#!/bin/bash

../user_setenv.sh

### check the AUTH folder
echo "auth folder : " $AUTH_FOLDER

### create a unencrypted yaml file with the AWS creds as variables from an AWS cvs creds file
python3 cvs_creds2yml_creds.py

### encrypt yaml AWS creds file
ansible-vault encrypt aws_creds_encrypted.yml --vault-password-file $AUTH_FOLDER/vault_pass.txt