from models import (
    connect_db, Image
)
from flask_debugtoolbar import DebugToolbarExtension

import os
from dotenv import load_dotenv
from flask import Flask, request
from AWS import AWS

app = Flask(__name__)

# toolbar = DebugToolbarExtension(app)

load_dotenv()

############ DB IMPORT CONFIG ###########################

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ['DATABASE_URL'].replace("postgres://", "postgresql://"))
app.config['SQLALCHEMY_ECHO'] = False
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
connect_db(app)


toolbar = DebugToolbarExtension(app)


############ AWS IMPORT CONFIG ###########################

app.config['S3_BUCKET'] = os.environ["AWS_BUCKET_NAME"]
app.config['S3_KEY'] = os.environ["AWS_ACCESS_KEY"]
app.config['S3_SECRET'] = os.environ["AWS_ACCESS_SECRET"]

BUCKET_NAME = os.environ["AWS_BUCKET_NAME"]


############################# Image Upload ################################

@app.route('/upload', methods=["POST"])
def upload_image():
    """ Handle image upload. Adds image and returns data about new image.
    """
    image = request.files['image']
    print('image from route', image)

    # NOTE: request.form gives us the other data in the multipart request (ex: request.form['filename'])

    image.key = Image.get_unique_key(image.filename)

    uploaded_image = AWS.upload(image, BUCKET_NAME)

    url = uploaded_image

    return {"url": url}


# verbose version - multi part, breaks into chunks
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


############################## Image Modification ###########################
