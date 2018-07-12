#!/bin/bash

source ../../user_setenv.sh

### check the AUTH folder
echo "auth folder : " $AUTH_DIR
echo "yggdrasil folder : " $YGG_HOME

### create a unencrypted yaml file with the AWS creds as variables from an AWS cvs creds file
python3 $YGG_HOME/security/cvs_creds2yml_creds.py $AUTH_DIR/$AWS_CREDS $AUTH_DIR/${AWS_CREDS%.csv}_unencrypted.yml

### copy the creds file to encrypt
cp $AUTH_DIR/${AWS_CREDS%.csv}_unencrypted.yml $AUTH_DIR/${AWS_CREDS%.csv}_encrypted.yml 

### encrypt yaml AWS creds file
ansible-vault encrypt $AUTH_DIR/${AWS_CREDS%.csv}_encrypted.yml --vault-password-file $AUTH_DIR/personal_vault_pass.txt

### create a Terraform AWS creds variables file stored in AUTH dir
python3 $YGG_HOME/security/cvs_creds2tf_creds.py $AUTH_DIR/$AWS_CREDS $AUTH_DIR/${AWS_CREDS%.csv}.tfvars