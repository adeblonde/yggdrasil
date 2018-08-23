# Yggdrasil

Yggdrasil is a project aimed at infrastructure automation. It integrates hosts provisioning, machine configuration, tools deployment and task execution into a single tool. Yggdrasil is mainly a python wrapper around DevOps automation tools called Ansible and Terraform.

## Main principles

Using a single configuration file in yaml syntax describing your infrastructure, groups of hosts and physical/virtual machines, and associated list of tasks, Yggdrasil can :

- provision the host machines you described on the cloud of your choice, using credentials you provided, by wrapping Terraform, a well-known devops tool
- send/receive data to these machines
- execute list of tasks simultaneously and/or by pools of worker machines, using Ansible, another well-known devops tool

During its execution, Yggdrasil will create, in a so-called 'work folder' you define :

- a Terraform config file, describing the infrastructure you desire in Terraform syntax
- a Terraform state file, describing the state of your infrastructure as created on the cloud you chose, storing for example associated public IP addresses
- an Ansible tree structure and playbook files, listing all the automated tasks you defined in the initial configuration file

## Why use Yggdrasil ?

You can think of Yggdrasil as a redundant tool for various reasons :

- Terraform is already a very complete tool for describing infrastructure-as-code and provisioning virtual machines on any cloud
- Ansible also provides tools for provisioning virtual machines on some cloud (especially Amazon Web Services) and collecting information about them

So why use Yggdrasil ? Here are the main reasons :

- Terraform as a whole is better suited than Ansible to manage infrastructure-as-code. Especially, Terraform can combine seamlessly many different cloud providers. Terraform also provides a very powerful and complete way to store the current state of your infrastructure, as a Terraform state file. Performing similar things with Ansible is more complex and needs lots of scripting. On the other side, Terraform does not provide a way to execute long list of tasks on remote hosts, which is exactly the main function of Ansible. Yggdrasil allows to combien the best of these two tools.
- Yggdrasil is NOT a closed environment. In fact, you can use Yggdrasil to generate a Terraform configuration file, an Ansible tasks tree, then run Terraform and Ansible completely independently from Yggdrasil in the work folder it generated. Yggdrasil is simply a workspace preparation tool.

## How does it work

Let us take a close look at an Yggdrasil configuration file to understand how it works :

```yaml
---
  config_name : test_config
```

Here is the name of your configuration, that will be used as the name of your work folder

```yaml
  parameters :
    - AUTH_DIR
    - CRED_FILE
    - SSH_KEY
    - AMI_ID
    - USERNAME
    - WORK_DIR
    - SCENARIO_NAME
    - VAULT_PSSWD
    - CODE_DIR
```

Here is the list of unset parameters of the configuration file. You will need to provide a parameters file as a input to Yggdrasil when executing it

```yaml
  ansible_resources :
    vault_password_file : 'AUTH_DIR/VAULT_PSSWD'
    vault_dir : 'AUTH_DIR'
    do_encrypt : false

  terraform_resources :
    credentials_dir : 'AUTH_DIR'
```

Here are some special resources needed by Ansible and Terraform.

Ansible has a security feature called Vault, that allows to encrypt secret parameters and use them as encrypted files in Ansible processes.
The `do_encrypt` option simply activate/deactivate the encryption process of secret files.
The `vault_password_file` is a plain text file storing the encryption password used by Ansible, the `vault_dir` is the directory where Yggdrasil will store the encrypted version of the secret file. You MUST have read/write access to this folder if using `do_encrypt`.

```yaml
  infrastructure :
    terraform_init : false
    terraform_plan : false
    terraform_apply : false
    terraform_refresh : false
    private_ssh_key_path : 'AUTH_DIR/SSH_KEY.pem'
```

The `infrastructure` key allows you to define the machines you wish to deploy.
Terraform allows several execution option, that you can activate/deactivate :

- `terraform_init` : At first execution in a folder, Terraform needs to download various files and initialize them. You must activate it at first run of you configuration. Terraform can detect when an initialization has already been runned, but you can skip this step after first run to save some time during execution
- `terraform_plan` : Terraform allows to execute 'dry runs' of a configuration, to visualize what your cloud provider will do. You can skip this step if you are confident in your configuration, otherwise the 'visualization' will be printed in the log file of Yggdrasil (written in your current working director)
- `terraform_apply` : When activated this option will effectively create your infrastucture
- `terraform_refresh` : When Terraform has already created your infrastructure, but you want to resynchronize the real infrastructure with your Terraform state file. Not needed if your are 'applying' Terraform already
  
Most cloud providers demands to use an SSH key to connect to the hosts you will create. For AWS for example, this key can be generated on the GUI console and downloaded manually. Even if you use only on-premises machines, it is strongly advised to access them using an SSH key, for obvious security reasons. So you must provide the path to your private SSH key in `private_ssh_key_path` option

```yaml
    providers :
    - provider :
        provider_name : aws
        region : 'eu-west-1'
        profile : developer
        credentials_file : 'AUTH_DIR/CRED_FILE'
        ssh_key : 'SSH_KEY'
```

In `providers` you define all the cloud providers you plan to use. For the momenet, only AWS is implemented.
The `credentials_file` is the csv file containing the keys for programmatic acces to AWS API, that you can download in the IAM field of AWS.

The file must have the following structure : 

```text
User name,Password,Access key ID,Secret access key,Console login link
XXX,XXX,XXX,XXX,XXX
```

Be sure to keep the data on two lines, one for the fields name, one for the actual values.

```yaml
        machines :
        - machine :
            name : master_machine
            user : ubuntu
            number : 1
            groups :
              - master
              - front
            aws_specs :
              AMI : AMI_ID
              type : t2.small
              region : 'eu-west-1'
              security_group : 'basic_sec_group'
```

In `machines` you can describe the various kinds of machines you want to create, with their number, the username, groups tags to identify them for Ansible scripts, and custom cloud parameters. If using AMI from AWS, be sure that the username you provide is the same as the username needed by the AMI, otherwise you won't be able to log in to the machine

```yaml
  data_sending :
    - data :
        origin : 'WORK_DIR/SCENARIO_NAME/test.txt'
        destination : '/home/ubuntu'
        isfolder : False
        by_names :
          - master_machine_0
          - worker_machine_0
        by_groups :
          - master
          - server

  data_receiving :
    - data :
        origin : 'WORK_DIR/SCENARIO_NAME/test.txt'
        destination : '/home/ubuntu'
        isfolder : False
        by_names :
          - master_machine_0
          - worker_machine_0
        by_groups :
          - master
          - server
```

You can define data to send to the machines or receive from them. Each `data` key is a file or folder to send/receive. You must specify if the item is a folder or file using the `isfolder` key. You can identify the target machines either by names or by groups tags

```yaml
  extra_job_folders :
    - 'CODE_DIR/yggdrasil/test'
  sync_jobs :
    job_list :
      - job :
          name : test_single_job
          target :
            - master_machine_0
          scripts :
            - playbook_test.yml
      - job :
          name : test_group_job
          target :
            - worker
          scripts :
          - playbook_test.yml
  pool_jobs :
    job_list :
      - job :
          name : test_pool_job
          type : pool
          target :
            - worker
          scripts :
            - playbook_test_1.yml
            - playbook_test_2.yml
```

In this part, you define the tasks that will be launched on your infrastructure.
These tasks are Ansible's 'playbooks', written in yaml syntax. Yggdrasil will create in your work folder a subfolder called `ansible`, containing an Ansible tasks tree as described in Ansible's best practices : [https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html]

Once your infrastructure is created by Terraform and available, Yggdrasil parses the Terraform state file to collect public IP addresses of your hosts, and creates a hosts file in your Ansible tasks tree. Ansible playbooks are runned against the hosts defined on this hosts file. All created machines are identified by the `name` of their configuration in the `machines` key, followed by an underscore and a number between 0 and the number of machines with the same configuration.

`sync_jobs` defines the tasks that will be synchronously by target or group of targets. It is the common use case of Ansible. `pool_jobs` is a custom use case, where you define a list of tasks to be executed by a pool of worker machines. In this case, Yggdrasil creates a queue of tasks to be executed, each task being an Ansible playbook, and a pool of threads, each thread being a worker machine.

For each `job` in the `job_list`, you define a `name` (used by the Ansible tasks tree), a `target` (full machine names or machine groups), and a list of `scripts`, i.e. Ansible playbooks.

You can use playbooks listed in the sources of Yggdrasil (`yggdrasil/yggdrasil/playbooks`) or in the folders defined in the list `extra_job_folders`

```yaml
  options :
    shutdown_after_complete : false
    data_only : false
    no_data : false
```

Here are some special options for Yggdrasil (not yet implemented) :

- `shutdown_after_complete` : destroy all cloud machines after the execution of all tasks
- `data_only` : use Yggdrasil only to send/receive data to remote hosts. All other actions are deactivated (Terraform & Ansible) (useful to avoid complex scp command line actions)
- `no_data` : do not send/receive data. This part of Yggdrasil is deactivated (useful when sending huge data files only once)
