import sys
import os
import logging

def create_logger(logfile='') :

    """ this function create a nice logger object """

    if logfile == '' :
        logfile = os.getcwd()
        logfile = os.path.join(logfile,'yggdrasil.log')

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # create a file handler
    handler = logging.FileHandler(logfile)
    handler.setLevel(logging.INFO)

    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(handler)

    logger.info('Logger created')

    return logger

def load_aws_credentials(logger, aws_creds_file) :

    """ this function loads the AWS credentials from a file into a dictionary """

    aws_creds = dict()

    try :
        with open(aws_creds, 'r') as f_read :
            data = f_read.read().split(',')
            aws_creds['aws_acces_key_id'] = data[2]
            aws_creds['aws_secret_key'] = data[3]
    except Exception as e :
        logger.info('The input file does not exist or cannot be read : error %s' % e)

    return aws_creds