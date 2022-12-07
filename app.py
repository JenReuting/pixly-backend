""" SQLAlchemy models for Pixly """

import os
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import boto3

# from flask_debugtoolbar import DebugToolbarExtension

# from models import (
#     db, connect_db, Image
# )

load_dotenv()

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URL'] = os.environ['DATABASE_URL'].replace("postgres://", "postgresql://")


app.config['S3_BUCKET'] = os.environ["AWS_BUCKET_NAME"]
app.config['S3_KEY'] = os.environ["AWS_ACCESS_KEY"]
app.config['S3_SECRET'] = os.environ["AWS_ACCESS_SECRET"]
app.config['S3_LOCATION'] = 'http://{}.s3.amazonaws.com/'.format(os.environ["S3_BUCKET_NAME"])
# toolbar = DebugToolbarExtension(app)

BASE_URL = 'https://pixlyapp.s3-us-west-1.amazonaws.com/'

# connect_db(app)

############ AWS IMPORT CONFIG ###########################

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.environ["AWS_ACCESS_KEY"],
    aws_secret_access_key=os.environ["AWS_ACCESS_SECRET"]
)
response = s3.list_objects(Bucket=os.environ["AWS_BUCKET_NAME"])
files = response.get("Contents")

for file in files:
    print(f"file_name: {file['Key']}, size: {file['Size']}")

############################# Image Upload / Serving ################################

# @app.route('/upload', methods=["POST"])
# def upload_image():
    """ Handle image upload. Adds image and returns data about new image.

    Get new image data (as Base64), upload image to AWS, get AWS link,
    creates new image instance in db, respond with AWS link.

    """

    # if "image" not in request.files:
    #     return "No image in request.files"

    # file = request.files["image"]

    # if file.filename == "":
    #     return "Please select an image to upload"

    # if file:
    #     file.filename = secure_filename(file.filename)
    #     output = send_to_s3(file, app.config["S3_BUCKET"])
    #     return str(output) ##should be url

    # if file:
    #     output = upload_file_to_s3(file)

    #     #if upload success, return name of uploaded file
    #     if output:
    #         print("file successfully uploaded! ")
    #         return jsonify(output)

    #data = request.json

    # call to AWS api - get image link

# def upload_file_to_s3(file, acl="public-read"):

    # filename = secure_filename(file.filename)


    # with open(file, "rb") as f:
    #     s3.upload_fileobj(f, os.environ["AWS_BUCKET_NAME"], "test_filename")



    # try:
    #     s3.upload_fileobj(
    #         file,
    #         os.getenv("AWS_BUCKET_NAME"),
    #         "test_filename",
    #         # ExtraArgs={
    #         #     "ACL":  acl,
    #         #     "ContentType": file.content_type
    #         # }
    #     )

    # except Exception as e:
    #     # A catchall exception
    #     print("Something isn't working: ", e)
    #     return e

    # return file
    # return file.filename

# TEST_FILE = open('./test5.jpg', "rb")

# upload_file_to_s3('./test5.jpg')



############################## Image Modification ###########################