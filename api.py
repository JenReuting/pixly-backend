from app import s3
from werkzeug.utils import secure_filename

import boto3
from boto3.s3.transfer import TransferConfig
from botocore.exceptions import ClientError


class AWS_Api:
    ''' Interact with AWS API '''

    @classmethod
    def upload(self, file, bucket: str, key: str) -> bool:
        '''
        Uploads a file to S3 bucket.

            Params:
                file: File to upload
                bucket: target s3 Bucket
                key: identifier, uses filename if not supplied.
            Returns:
                True if successful upload, else False
        '''

        try:
            with open(file, 'rb') as f:
                s3.upload_fileobj(f, bucket, key)
        except ClientError as error:
            print(error)
            return False
        return True
