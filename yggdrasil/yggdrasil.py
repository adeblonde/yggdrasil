from common_tools import *
from terraform.aws import *
from ansible_resources.ansible_setting import *
# from ansible_templates import *
import os
import sys
import yaml
import fileinput
import shutil
import pkg_resources
import copy
import json
import click
from os.path import join

# import python_terraform as tf
from python_terraform import *

import pdb

DATA_PATH = pkg_resources.resource_filename('yggdrasil', '.')

ami2user = {
	'ami-2a7d75c0' : 'ubuntu'
}

@click.command()
@click.argument('configfile', default='./yggdrasil_config.yml',help='Path to yggdrasil configuration file')
@click.option('--shutdownatend','-s', default=False,help='Do you want to shutdown host machines after execution of all jobs ?')
@click.option('--dryrun','-d', default=False,help='Execute a dry run of the Terraform configuration, Ansible jobs won\'t be executed')
@click.option('--workfolder','-w', default='.',help='Location of the working folder that will be created with temporary file, name after \'config_name\'')
def ygg(configfile, workfolder, dryrun=False, shutdownatend=False) :

	""" we execute the run options with the provided arguments """
	run(configfile, workfolder, dryrun=False, shutdownatend=False)

@click.command()
@click.argument('configfile', help='Yggdrasil YAML configuration file to set')
@click.option('--output','-o', help='Yggdrasil YAML configuration file set')
@click.option('--params','-f', help='JSON file with all the parameters to set in the Yggdrasil\'s configuration file')
@click.option('--variable','-v', type=(unicode, unicode), multiple=True)
def ygg_config(configfile, output, params, variable):

	""" this function is used to set the variables in an Yggdrasil's unset configuration file """
	with open(configfile) as f :
		config = f.read()

	if output is None :
		output = os.getcwd()
		output_name = os.path.basename(configfile)
		output_name = 'set_' + output_name
		output = join(output, output_name)

	output_folder = os.path.dirname(output)
	makedir_p(output_folder)

	parameters = dict()

	if params is not None :
		with open(params) as f :
			parameters = json.load(f)

	if variable is not None :
		for key, value in variable :
			parameters[key] = value

	for param in parameters.keys() :
		config = config.replace(param, parameters[param])

	with open(output, 'w') as f :
		f.write(config)

def run(configfile, workfolder, dryrun=False, shutdownatend=False) :

	""" the run function is separated from the main CLI function ygg, for modularity purposes """

	""" main yggdrasil function """
	print("Begin execution of Yggdrasil!")

	work_dir = workfolder

	""" init logger """
	logger = create_logger(join(work_dir,'ygg.log'))

	""" parse config file """
	with open(configfile) as f :
		config = yaml.load(f)

	""" create work folder """
	if os.path.exists(work_dir) is False :
		os.makedirs(work_dir)

	""" Terraform part """
	logger.info("Terraform part")

	""" init terraform config file """
	tf_config = ''

	""" prepare Terraform config file """
	for provider in config['infrastructure']['providers'] :
		provider = provider['provider']

		if provider == 'aws' :

			logger.info("Creating AWS config file")
			tf_config = terraform_set_aws(logger, DATA_PATH, work_dir, config)

	with open(join(work_dir, config['config_name'] + '.tf'), 'w') as f :
		f.write(tf_config)

	# """ run Terraform """
	# logger.info("Run Terraform")
	# tf = Terraform(working_dir=work_dir)
	# print(tf.init())
	# logger.info("Terraform loaded")
	# logger.info("Planning")
	# print(tf.plan(no_color=IsFlagged, refresh=False, capture_output=True))
	# if dryrun == False :
	# 	logger.info("Applying")
	# 	print(tf.apply(no_color=IsFlagged, refresh=False, skip_plan=True))

	""" Ansible part """
	logger.info("Ansible part")

	""" we parse the .tfstate file to gather public IPs addresses """
	logger.info("Parsing .tfstate")
	host_ips, host_usernames, group_hosts = gather_ips(work_dir, ami2user, logger)

	""" create Ansible config tree """
	logger.info("Creating Ansible config tree")
	ansible_dir, ansible_production_dir, ansible_roles_dir = create_config_tree(logger, work_dir)

	""" create hosts file """
	logger.info("Creating Ansible hosts file")
	production_hosts_path = create_host_file(logger, config, host_ips, group_hosts, ansible_production_dir)

	""" set an SSH connection that will accept unknown hosts """	
	logger.info("Setting SSH connection""")
	ssh = set_ssh_connection()

	""" sending data to hosts """
	logger.info("Sending data to remote hosts")
	scp_data(ssh, logger, host_ips, group_hosts, host_usernames, config, 'sending')

	""" collect all ansible playbooks paths """
	logger.info("Collecting all ansible playbooks paths")
	modules_playbooks = join(DATA_PATH, 'playbooks')
	playbooks_folder = [modules_playbooks]
	playbooks_path = collect_playbooks_paths(logger, config, playbooks_folder)

	""" collecting all synchronous jobs """
	logger.info("Collecting all synchronous jobs")
	main_ansible_path = collect_synchronous_jobs(logger, config, ansible_roles_dir, ansible_dir, playbooks_path)

	""" Execution of synchronous jobs """
	logger.info("Executing Ansible synchronous tasks")
	try :
		result = subprocess.call(['/usr/bin/ansible-playbook', '-i', production_hosts_path, main_ansible_path])
		logger.info("Result of ansible call : %s" % result)
	except :
		logger.info("Problem in the execution of ansible playbooks")

	""" implementing workers pool jobs """
	logger.info("Collecting Ansible asynchronous tasks")
	processes = prepare_pool_jobs(logger, config, ansible_dir, production_hosts_path, playbooks_path, group_hosts)

	logger.info("Executing Ansible asynchronous tasks")
	for p in processes :
		p.start()

	for p in processes :
		p.join()

	""" receiving from to hosts """
	logger.info("Receiving data from remote hosts")
	scp_data(ssh, logger, host_ips, group_hosts, host_usernames, config, 'receiving')

if __name__ == "__main__" :
	run(sys.argv[1], sys.argv[2])