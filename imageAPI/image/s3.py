import boto3
from botocore.config import Config

my_config = Config(
    region_name='eu-west-2',
    signature_version='v4',
    retries={
        'max_attempts': 10,
        'mode': 'standard'
    }
)

s3_client = boto3.client('s3', config=my_config)
