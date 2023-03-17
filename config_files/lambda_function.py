import json

import boto3
import os
import sys
import uuid
from urllib.parse import unquote_plus
from PIL import Image
import PIL.Image

s3_client = boto3.client('s3')


def resize_image(image_path, resized_path, size):
    size = int(size)
    with Image.open(image_path) as image:
        image.thumbnail((size, size))
        image.save(resized_path)


def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        tmpkey = key.replace('/', '')
        user, filename = key.split('/')
        metadata = s3_client.head_object(Bucket=bucket, Key=key)['Metadata']
        download_path = f'/tmp/{uuid.uuid4()}{tmpkey}'
        thumbnail_sizes = metadata['sizes'].strip('][').split(', ')
        for size in thumbnail_sizes:
            size_key = user + "/" + str(size) + filename
            s3_client.download_file(bucket, key, download_path)
            upload_path = f'/tmp/{bucket}_{tmpkey}'
            resize_image(download_path, upload_path, size)
            s3_client.upload_file(upload_path, bucket + "-resized", size_key)
