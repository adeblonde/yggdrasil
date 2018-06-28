# Yggdrasil

Yggdrasil is a project aimed at Data Workflow Automation. It integrates hosts provisioning, machine configuration, tools deployment and setup, to create a full stack of database/Machine Learning Sandbox/Rest consumption API/GUI dashboard and supervision.

Yggdrasil wraps various open source tools with python and shell scripts. These tools are mainly :

- Ansible
- Terraform
- Docker
- Swagger

Yggdrasil is designed to suit small-scale infrastructures and clusters, especially for developers and AI engineers. If you plan to create a large-scale cluster for persistent production services, you should prefer DCOS, which is a cluster manager tool able to provide such services. Nevertheless, many tools included in Yggdrasil will be made available for DCOS too.

Yggdrasil is made of the following modules :

- Provisioning
- Task manager
- ETL
- Machine Learning Agent
- Dashboard
- API deployment
- Database deployment

## Provisioning module

The provisioning module is a wrapper of Terraform, an open source tool developped by HashiCorp that allows to provision hosts on a large list of cloud providers using CLI inputs and YAML configuration files.

## Task manager

The task manager module is a wrapper of Ansible, an open source tool that allows to launch distributed CLI commands simultaneously on an arbitrarily large number of remote hosts through SSH.

## ETL

The ETL module is a template for Spark jobs, that can load data from various data sources (SQL Server, MySQL/MariaDB, PostgreSQL, AWS S3, etc, local filesystem) process them with Spark, and push them on other various data sources

## Machine Learning Agent

The Machine Learning Agent is a service which runs on a dedicated host, generally including a GPU, and listening to a message broker for executing various ML jobs (learning models from standard use case, providing applications from trained models)

## Dashboard

The Dashboard is a simple ReactJS graphical frontend for monitoring all of your jobs and devices

## API deployment

The API deployment module use the OpenAPI description standard and the Swagger CodeGen tool to automatically generate and deploy Rest APIs from a well-designed configuration file.

## Database deployment

The database deployment is a special use case of the Task manager designed for deploying common databases (PostgreSQL, MariaDB, MongoDB)