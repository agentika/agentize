from __future__ import annotations

import json
import logging
import os
import time
from datetime import datetime
from io import BytesIO
from pathlib import Path

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


def _upload_object(content: str, file_name: str) -> bool:
    """Upload a file to an S3 bucket.

    Args:
        content(str) : The content to upload.
        file_name (str): file name. If not specified then unix timestamp is used.

    Returns:
        bool: True if file was uploaded, else False
    """
    file_obj_bytes = BytesIO(content.encode("utf-8"))
    bucket = os.getenv("AWS_BUCKET_NAME")
    if bucket is None:
        raise ValueError("AWS_BUCKET_NAME environment variable not set")

    # If file_name was not specified, use unix timestamp for object name
    if file_name is None or file_name == "":
        # Use the current unix timestamp as the object name remove floa<ting point
        timestamp = int(time.time())
        # Convert the timestamp to a string
        file_name = str(timestamp)
    else:
        # Remove the file extension from the file name
        file_name = Path(file_name).stem

    # Use the specified file name. upload path yy-mm-dd/<File Name>
    object_name = f"{datetime.now().strftime('%y-%m-%d')}/{file_name.lower()}"

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


def upload_markdown(title: str, content: str, file_name: str) -> bool:
    """Upload markdown file to an S3 bucket.
    Args:
        title (str): The title of the page.
        content(str) : The markdown content to upload.
        file_name (str): The file name. If not specified then unix timestamp is used.

    Returns:
        bool: True if file was uploaded, else False
    """

    safe_md = json.dumps(content)
    # convert markdown to html
    html = HTML_TEMPLATE.format(title=title, md=safe_md)
    return _upload_object(html, file_name)


upload_markdown_tool = function_tool(upload_markdown)
