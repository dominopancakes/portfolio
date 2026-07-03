import psycopg2 
import boto3
import logging
import json

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

# create client for the SSM (Systems Manager) service. Allows API calls to SSM Parameter Store
ssm_client = boto3.client('ssm')

# Get the SSM Param from AWS and turn it into JSON
def get_ssm_param(param_name):
    LOGGER.info(f'get_ssm_param: getting param_name={param_name}')
    parameter_details = ssm_client.get_parameter(Name=param_name)
    redshift_details = json.loads(parameter_details['Parameter']['Value'])

    host = redshift_details['host']
    user = redshift_details['user']
    db = redshift_details['database-name']
    LOGGER.info(f'get_ssm_param: loaded for db={db}, user={user}, host={host}')
    return redshift_details

def get_connection_and_cursor(redshift_details):
    try:
        connection = psycopg2.connect(
            host=redshift_details['host'],
            port=redshift_details['port'],
            dbname=redshift_details['database-name'],
            user=redshift_details['user'],
            password=redshift_details['password']
        )

        cursor = connection.cursor()

        LOGGER.info(f'get_connection_and_cursor: connection ready')
        return connection, cursor

    except ConnectionError as e:
        LOGGER.info(f'get_connection: failed to open connection: {e}')
        raise e



