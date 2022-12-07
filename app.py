import os
from dotenv import load_dotenv
from flask import Flask, request
from Aws import Aws
from Image import Image

# from flask_debugtoolbar import DebugToolbarExtension
app = Flask(__name__)

# from models import (
#     db, connect_db, Image
# )

# toolbar = DebugToolbarExtension(app)
# connect_db(app)
load_dotenv()


app.config['SQLALCHEMY_DATABASE_URL'] = os.environ['DATABASE_URL'].replace("postgres://", "postgresql://")
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']


############ AWS IMPORT CONFIG ###########################

app.config['S3_BUCKET'] = os.environ["AWS_BUCKET_NAME"]
app.config['S3_KEY'] = os.environ["AWS_ACCESS_KEY"]
app.config['S3_SECRET'] = os.environ["AWS_ACCESS_SECRET"]

BUCKET_NAME=os.environ["AWS_BUCKET_NAME"]




############################# Image Upload ################################

@app.route('/upload', methods=["POST"])
def upload_image():
    """ Handle image upload. Adds image and returns data about new image.
    """
    image = request.files['image']

    # NOTE: request.form gives us the other data in the multipart request (ex: request.form['filename'])

    image.key = Image.get_unique_key(image.filename)
    uploaded_image = Aws.upload(image)

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
