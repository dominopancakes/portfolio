import boto3
import logging

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

s3_client = boto3.client('s3')

def get_file_info(event):

    LOGGER.info('get_file_info: starting')
    first_record = event['Records'][0]
    bucket_name = first_record['s3']['bucket']['name']
    file_name = first_record['s3']['object']['key']

    LOGGER.info(f'get_file_info: file={file_name}, bucket_name={bucket_name}')

    return bucket_name, file_name

def create_s3_object(bucket_name, s3_key):

    s3_object = s3_client.get_object(
        Bucket=bucket_name,
        Key=s3_key
    )

    return s3_object