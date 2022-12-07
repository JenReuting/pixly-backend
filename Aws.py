from werkzeug.utils import secure_filename
from botocore.exceptions import ClientError
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.environ["AWS_ACCESS_KEY"],
    aws_secret_access_key=os.environ["AWS_ACCESS_SECRET"]
)

BUCKET_NAME=os.environ["AWS_BUCKET_NAME"]
S3_BASE_URL = f'https://{BUCKET_NAME}.s3.amazonaws.com/'


class Aws:
    ''' Interact with AWS API '''

    # Fetch file from AWS

    @classmethod
    def signed_url(self, bucket_name, key, expires=3600):
        '''
        Fetch signed URL from AWS S3.
            Params:
                bucket_name: target s3 bucket
                key: name as stored on s3
                expires: in seconds
            Returns: string
        '''

        url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': bucket_name, 'Key': key},
            ExpiresIn=expires)

        return url

    @classmethod
    def object_url(self, bucket_name, key):
        ''' Construct Object URL -> requires read access '''
        return f'https://{bucket_name}.s3.us-west-1.amazonaws.com/{key}'

    @classmethod
    def download(self, bucket_name, file_name, key=None):
        '''
        Download a file from S3.

            Params:
                bucket_name: target s3 bucket
                file_name: OUTPUT file_name
                key: name as stored on s3

            '''

        if key is None:
            key = file_name

        try:
            with open(file_name, 'wb') as file:
                file = s3.download_fileobj(
                    BUCKET_NAME,
                    key,
                    file
                )
                return ('file', file)
        except ClientError as error:
            print(error)
            return False

    @classmethod
    def upload(self, file):
        '''
        Uploads a file to S3 bucket.

            Params:
                file_name: File to UPLOAD (binary)
                bucket: target s3 Bucket
                key: s3 name -> defaults to file_name if not supplied.
                metadata: optional key: value pair
            Returns:
                True if successful upload, else False
        '''


        print("file from AWS class -----> ", file)


        try:
            s3.upload_fileobj(
                file,
                BUCKET_NAME,
                file.key)

        except ClientError as error:
            print(error)
            return {"errors": str(error)}

        return f"{S3_BASE_URL}{file.key}"

        # try:
        #     # with open(file_name, 'rb') as file:
        #     s3.upload_fileobj(
        #         file,
        #         bucket_name,
        #         key,
        #         ExtraArgs={
        #             'Metadata': metadata})
        # except ClientError as error:
        #     print(error)
        #     return False
        # return f"{S3_BASE_URL}{file.key}"