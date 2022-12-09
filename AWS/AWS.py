from botocore.exceptions import ClientError
import boto3
import os

from dotenv import load_dotenv

load_dotenv()

s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.environ["AWS_ACCESS_KEY"],
    aws_secret_access_key=os.environ["AWS_ACCESS_SECRET"]
)


class AWS:
    ''' Interact with AWS API '''

    @classmethod
    def get_object(self, file_name, bucket_name):
        print('AWS -> get_object', file_name, bucket_name)
        s3_response_object = s3_client.get_object(
            Bucket=bucket_name, Key=file_name)
        return s3_response_object

    @classmethod
    def create_bucket(self, bucket_name, region='us-west-1'):
        '''' Create a new bucket on S3

            If a region is not specified, the bucket is created in the S3 default
            region (us-east-1).

                Params:
                    bucket_name: Bucket to create
                    region: String region to create bucket in, e.g., 'us-west-2'
                Returns:
                    True if created, else false

        '''

        try:
            s3_client.create_bucket(Bucket=bucket_name)
        except ClientError as e:
            print('create_bucket ERROR', e)
            return False
        return True

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

        url = s3_client.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': bucket_name, 'Key': key},
            ExpiresIn=expires)

        return url

    @classmethod
    def object_url(self, bucket_name, key):
        ''' Construct Object URL -> requires read access '''
        return f'https://{bucket_name}.s3.amazonaws.com/{key}'

    @classmethod
    def download(self, bucket_name, file_name):
        '''
        Download a file from S3.

            Params:
                bucket_name: target s3 bucket
                file_name: OUTPUT file_name
                key: name as stored on s3

            '''

        # if key is None:
        #     key = file_name

        try:
            with open(file_name, 'wb') as file:
                file = s3_client.download_fileobj(
                    bucket_name,
                    file_name,
                    file
                )
                return ('file', file)
        except ClientError as error:
            print(error)
            return False

    @classmethod
    def upload(self, file, bucket_name, file_name, ext):
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
        print(file)
        try:
            s3_client.upload_fileobj(
                file,
                bucket_name,
                file_name,
                ExtraArgs={
                    'ContentType': 'image/jpeg'
                }
            )
            print(f' -----> BACKEND API - AWS S3 -----> Image uploaded')
            return True

        except ClientError as error:
            print(error)
            return {"errors": str(error)}
