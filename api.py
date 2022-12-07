from werkzeug.utils import secure_filename
from botocore.exceptions import ClientError
from app import s3_resource, s3_client


class AWS_api:
    ''' Interact with AWS API '''

    # Fetch file from AWS

    @classmethod
    def download(self, bucket_name, file_name, object_name=None):
        '''
        Download a file from S3.

            Params:
                bucket: target s3 bucket
                file_name: OUTPUT file_name
                object_name: name as stored on s3

            '''

        if object_name is None:
            object_name = file_name

        try:
            with open(file_name, 'wb') as file:
                file = s3_client.download_fileobj(
                    bucket_name,
                    object_name,
                    file
                )
                return ('file', file)
        except ClientError as error:
            print(error)
            return False

    @classmethod
    def upload(self, file_name, bucket_name, object_name=None, metadata={}) -> bool:
        '''
        Uploads a file to S3 bucket.

            Params:
                file_name: File to UPLOAD (binary)
                bucket: target s3 Bucket
                object_name: s3 name -> defaults to file_name if not supplied.
                metadata: optional key: value pair
            Returns:
                True if successful upload, else False
        '''

        if object_name is None:
            object_name = file_name

        try:
            with open(file_name, 'rb') as file:
                s3_client.upload_fileobj(
                    file,
                    bucket_name,
                    object_name,
                    ExtraArgs={
                        'Metadata': metadata})
        except ClientError as error:
            print(error)
            return False
        return file_name

    # Update
