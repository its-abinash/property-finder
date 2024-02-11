import logging
import boto3
from django.conf import settings
import uuid
logger = logging.getLogger(__name__)
logger.setLevel("INFO")


class FileUploadService:

    @classmethod
    def upload_media_file(cls, file=None, content_type=None, file_name=None):
        s3_client = boto3.client('s3', region_name=settings.AWS_STORAGE_REGION)
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        slug = str(uuid.uuid4().hex) + "/" + (file_name or "")
        upload_image_response = s3_client.put_object(ACL=settings.AWS_DEFAULT_ACL,
                                                        Body=file, Bucket=bucket_name,
                                                        Key=slug, ContentType=content_type)
        s3_response = upload_image_response.get('ResponseMetadata')
        if s3_response.get('HTTPStatusCode') == 200:
            return settings.S3_UPLOADED_FILE_URL.format(bucket_name=bucket_name,
                    region=settings.AWS_STORAGE_REGION, slug=slug)
        else:
            return None