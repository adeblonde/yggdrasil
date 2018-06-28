import boto3
import os
import sys

def create_s3_connection(logger, aws_creds) :

    """ this function create the S3 connection client associated with AWS creds """

    client = boto3.client(
        's3',
        aws_access_key_id=aws_creds['aws_acces_key_id'],
        aws_secret_access_key=aws_creds['aws_secret_key'],
    )

    return client
