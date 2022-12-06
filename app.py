""" SQLAlchemy models for Pixly """

import os
from dotenv import load_dotenv
from flask import Flask, request, redirect
from werkzeug.utils import secure_filename


import boto3
from boto3.s3.transfer import TransferConfig
from botocore.exceptions import ClientError

from flask_debugtoolbar import DebugToolbarExtension

from models import (
    db, connect_db, Image
)

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URL'] = os.environ['DATABASE_URL'].replace(
    "postgres://", "postgresql://")


app.config['S3_BUCKET'] = os.environ["S3_BUCKET_NAME"]
app.config['S3_KEY'] = os.environ["AWS_ACCESS_KEY"]
app.config['S3_SECRET'] = os.environ["AWS_ACCESS_SECRET"]
app.config['S3_LOCATION'] = 'http://{}.s3.amazonaws.com/'.format(
    os.environ["S3_BUCKET_NAME"])
toolbar = DebugToolbarExtension(app)

connect_db(app)

### UPLOAD CONFIG ##
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}


############ AWS IMPORT CONFIG ###########################

s3 = boto3.client(
    "s3",
    aws_access_key_id=app.config['S3_KEY'],
    aws_secret_access_key=app.config['S3_SECRET']
)

############################# Image Upload / Serving ################################


@app.route('/upload', methods=["POST"])
def api_upload_image():
    """ Handle image upload from front-end. Adds image and returns data about new image.

    Get new image data (as Base64), upload image to AWS, get AWS link,
    creates new image instance in db, respond with AWS link.

    """

    if "image" not in request.files:
        return "No image in request.files"

    file = request.files["image"]

    if file.filename == "":
        return "Please select an image to upload"

    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        s3.upload_file(
            Bucket=app.config["S3_BUCKET"],
            Filename=filename,
            Key=filename)
        # output = send_to_s3(file, app.config["S3_BUCKET"])
        return str()  # should be url
    else:
        return redirect('/')

    # data = request.json

    # call to AWS api - get image link


def allowed_file(filename):
    ''' Confirm uploaded image is correct file type.
    Accepts only JPG or JPEG files, and rejects others. Returns true/false
    '''
    return ('.' in filename
            and filename.rsplit('.', 1)[1].tolower()
            in ALLOWED_EXTENSIONS)


# def upload_file(file_name, bucket, object_name=None):
#     ''' Uploads the file to S3 bucket.

#         Params:
#             file_name: File to upload
#             bucket: target s3 Bucket
#             object_name: s3 object name. uses file_name if not specified
#         Return:
#             True if successful upload, else False
#     '''

#     # Use file_name if object_name not specified
#     if object_name is None:
#         object_name = os.path.basename(file_name)

#     # Handle upload
#     s3_client = boto3.client('s3')
#     try:
#         response = s3_client.upload_file(file_name, bucket, object_name)
#     except ClientError as error:
#         print(error)
#         return False
#     return True


############################## Image Modification ###########################
