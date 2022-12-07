""" SQLAlchemy models for Pixly """

import os
import io
# from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from flask import Flask, request
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

############################# Image Upload / Serving ################################

# @app.route('/upload', methods=["POST"])
# def upload_image():

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

def upload_file_to_s3(file, acl="public-read"):

    with open(file, 'rb') as data:
        s3.upload_fileobj(data, 'pixlyapp', 'newKeyWooHOO')


upload_file_to_s3('./test5.jpg')



############################## Image Modification ###########################