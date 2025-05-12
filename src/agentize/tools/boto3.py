from __future__ import annotations

import json
import logging
import os
import time
from io import BytesIO

import boto3
from agents import function_tool
from botocore.exceptions import ClientError

HTML_TEMPLATE = """<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <title>{title}</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.8.1/github-markdown-light.min.css">
</head>
<body>
  <div class="markdown-body" id="content"></div>
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <script>
    document.getElementById('content').innerHTML =
      marked.parse({md});
  </script>
</body>
</html>
"""


def _upload_object(title: str, content: str, object_name: str) -> bool:
    """Upload a file to an S3 bucket.

    Args:
        title (str): The title of the HTML page.
        content(str) : The content to upload.
        object_name (str): S3 object name. If not specified then unix timestamp is used.

    Returns:
        bool: True if file was uploaded, else False
    """
    file_obj_bytes = BytesIO(content.encode("utf-8"))
    bucket = os.getenv("AWS_BUCKET_NAME")
    if bucket is None:
        raise ValueError("AWS_BUCKET_NAME environment variable not set")

    # If S3 object_name was not specified, use unix timestamp
    if object_name is None or object_name == "":
        timestamp = int(time.time())
        object_name = str(timestamp)

    s3_client = boto3.client("s3")
    try:
        # Upload the file object
        s3_client.upload_fileobj(
            Fileobj=file_obj_bytes,
            Bucket=bucket,
            Key=object_name,
            # Content type is set to text/html
            ExtraArgs={
                "ContentType": "text/html; charset=utf-8",
            },
        )
    except ClientError as e:
        logging.error(e)
        return False
    return True


def upload_html(title: str, content: str, object_name: str) -> bool:
    """Upload HTML content to an S3 bucket.
    Args:
        title (str): The title of the HTML page.
        content(str) : The content to upload.
        object_name (str): S3 object name. If not specified then unix timestamp is used.

    Returns:
        bool: True if file was uploaded, else False
    """

    safe_md = json.dumps(content)
    html = HTML_TEMPLATE.format(title=title, md=safe_md)
    return _upload_object(title, html, object_name)


upload_html_tool = function_tool(upload_html)
