""" SQLAlchemy models for Pixly """

import os
from dotenv import load_dotenv
from flask import Flask, request
import boto3, botocore

from flask_debugtoolbar import DebugToolbarExtension

from models import (
    db, connect_db, Image
)

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URL'] = os.environ['DATABASE_URL'].replace("postgres://", "postgresql://")


app.config['S3_BUCKET'] = os.environ["S3_BUCKET_NAME"]
app.config['S3_KEY'] = os.environ["AWS_ACCESS_KEY"]
app.config['S3_SECRET'] = os.environ["AWS_ACCESS_SECRET"]
app.config['S3_LOCATION'] = 'http://{}.s3.amazonaws.com/'.format(os.environ["S3_BUCKET_NAME"])
toolbar = DebugToolbarExtension(app)

connect_db(app)

############ AWS IMPORT CONFIG ###########################

s3 = boto3.client(
    "s3",
    aws_access_key_id=app.config['S3_KEY'],
    aws_secret_access_key=app.config['S3_SECRET']
)

############################# Image Upload / Serving ################################

@app.route('/upload', methods=["POST"])
def upload_image():
    """ Handle image upload. Adds image and returns data about new image.

    Get new image data (as Base64), upload image to AWS, get AWS link,
    creates new image instance in db, respond with AWS link.

    """

    if "image" not in request.files:
        return "No image in request.files"

    file = request.files["image"]

    if file.filename == "":
        return "Please select an image to upload"

    if file:
        file.filename = secure_filename(file.filename)
        output = send_to_s3(file, app.config["S3_BUCKET"])
        return str(output) ##should be url

    #data = request.json

    # call to AWS api - get image link



############################## Image Modification ###########################