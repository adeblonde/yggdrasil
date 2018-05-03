from .common_tools import *
import os
import sys
import yaml
import fileinput
import shutil

import click

from python_terraform import * 

from os.path import join

import pdb

@click.command()
@click.option('--shutdownatend','-s',default=False,help='Do you want to shutdown host machines after execution of all jobs ?')
@click.option('--dryrun','-d',default=False,help='Execute a dry run of the Terraform configuration, Ansible jobs won\'t be executed')
@click.option('--configfile','-c',default='./yggdrasil_config.yml',help='Path to yggdrasil configuration file')
@click.option('--workfolder',default='.',help='Location of the working folder that will be created with temporary file, name after \'config_name\'')
def ygg(configfile, workfolder, dryrun, shutdownatend) :

    """ main yggdrasil function """
    print("Begin execution of Yggdrasil!")

    work_dir = workfolder

    """ init logger """
    logger = create_logger(join(work_dir,'ygg.log'))

    """ parse config file """
    with open(configfile) as f :
        config = yaml.load(f)
        print(config)

    """ create work folder """
    if os.path.exists(work_dir) is False :
        os.makedirs(work_dir)

    """ set cloud credentials """
    cloud_creds = dict()
    provider = config['infrastructure']['provider']
    tf_resources = ''

    if provider == 'aws' :
        cloud_creds = load_aws_credentials(logger, config['infrastructure']['credentials_file'])

        tf_resources = join(__file__, 'terraform_resources', 'aws')

        shutil.copyfile(join(tf_resources, 'aws_config_template'), join(work_dir, 'config'))
        shutil.copyfile(join(tf_resources, 'aws_credentials_template'), join(work_dir, 'credentials'))

        """ set the AWS config file """
        for line in fileinput.input(join(work_dir, 'config'), inplace=True) :
            print(line.replace('default',config['infrastructure']['profile']))
            print(line.replace('AWS_REGION',config['infrastructure']['region']))

        """ set the AWS credentials file """
        for line in fileinput.input(join(work_dir, 'credentials'), inplace=True) :
            print(line.replace('AWS_ACCESS_KEY',cloud_creds['aws_acces_key_id']))
            print(line.replace('AWS_SECRET_KEY',cloud_creds['aws_secret_key']))

    """ create the terraform config file """
    tf_config = ''
    if provider == 'aws' :

        with open(join(tf_resources, 'aws_header.tf'), 'r') as f :
            tf_header = f.read()

        with open(join(tf_resources, 'aws_instance.tf'), 'r') as f :
            tf_instance = f.read()

        tf_header.replace('AWS_ACCESS_KEY',cloud_creds['aws_acces_key_id']))
        tf_header.replace('AWS_SECRET_KEY',cloud_creds['aws_secret_key']))
        tf_header.replace('AWS_REGION',config['infrastructure']['region']))

        tf_config = tf_header

        for model in config['infrastructure']['machines'] :
            current_model = deepcopy(tf_instance)
            current_model.replace('NUMBER',model['number'])
            current_model.replace('AMI',model['aws_specs']['AMI'])
            current_model.replace('TYPE',model['aws_specs']['type'])
            tf_config += current_model

    with open(join(work_dir, config['config_name'] + '.tf'), 'w') as f :
        f.write(tf_config)

    """ run Terraform """
    t = Terraform(working_dir=work_dir)
    if dryrun == True :
        tf.test()
        return 
    else :
        tf.apply(no_color=IsFlagged, refresh=False)

    """ prepare .ini files for Ansible """

    """ add SSH certificates to known_hosts """

    """ send data to machines """

    """ apply ansible """









if __name__ == "__main__" :
    ygg()