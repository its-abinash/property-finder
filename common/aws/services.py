import logging
import os

import boto3
from django.conf import settings

logger = logging.getLogger(__name__)
logger.setLevel("INFO")


class FileUploadService:

    @classmethod
    def upload_media_file(cls, file=None, content_type=None, file_path=None,
                          document_type="public"):
        try:
            s3_client = boto3.client('s3', region_name=settings.AWS_STORAGE_REGION)
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            if document_type == "private":
                upload_image_response = s3_client.put_object(ACL="private",
                                                             Body=file, Bucket=bucket_name,
                                                             Key=file_path, ContentType=content_type)
            else:
                upload_image_response = s3_client.put_object(Body=file, Bucket=bucket_name,
                                                             Key=file_path, ContentType=content_type)
            s3_response = upload_image_response.get('ResponseMetadata')
            if s3_response.get('HTTPStatusCode') == 200:
                return {"status": "success", "data": str(s3_response)}
            else:
                return {"status": "error", "data": str(s3_response)}
        except Exception as e:
            return {"status": "error", "data": str(e)}