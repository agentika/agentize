from __future__ import annotations

import io
import logging
import time

import boto3
from agents import function_tool
from botocore.exceptions import ClientError


@function_tool
def upload_object(content: str, bucket: str, object_name: str) -> bool:
    """Upload a file to an S3 bucket
    Args:

        content(str) : The content to upload.
        bucket (str): Bucket to upload to.
        object_name (str): S3 object name. If not specified then SHA256 of the content is used.
    Returns:
        bool: True if file was uploaded, else False
    """
    file_obj = io.StringIO(content)

    # If S3 object_name was not specified, use unix timestamp
    if object_name is None or object_name == "":
        timestamp = int(time.time())
        object_name = str(timestamp)

    # Upload the file
    s3_client = boto3.client("s3")

    try:
        s3_client.upload_fileobj(
            Fileobj=file_obj,
            Bucket=bucket,
            Key=object_name,
            ExtraArgs={
                "ContentType": "text/markdown; charset=utf-8",
            },
        )
    except ClientError as e:
        logging.error(e)
        return False
    return True
