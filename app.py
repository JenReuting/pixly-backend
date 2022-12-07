import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, session
from PIL import Image
import uuid
import boto3
# from flask_debugtoolbar import DebugToolbarExtension
app = Flask(__name__)
from werkzeug.wrappers import Request, Response

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
S3_BASE_URL = f'https://{BUCKET_NAME}.s3.amazonaws.com/'
ALLOWED_EXTENSIONS={"jpg", "jpeg", "gif", "png"}

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.environ["AWS_ACCESS_KEY"],
    aws_secret_access_key=os.environ["AWS_ACCESS_SECRET"]
)

def allowed_file(filename):
    return "." in filename and \
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def get_unique_key(filename):
    ext = filename.rsplit(".", 1)[1].lower()
    uuid_key = uuid.uuid4().hex
    return f"{uuid_key}.{ext}"

############################# Image Upload ################################

@app.route('/upload', methods=["POST"])
def upload_image():
    """ Handle image upload. Adds image and returns data about new image.
    """
    image = request.files['image']

    # NOTE: request.form gives us the other data in the multipart request (ex: request.form['filename'])

    image.key = get_unique_key(image.filename)
    uploaded_image = upload_file_to_s3(image)


    url = uploaded_image

    return {"url": url}

    opened_image = Image.open(image.stream)
    print("Opened image from API body --------------->", opened_image)
    print("Image size from API body --------------->", opened_image.size)

    if "image" not in request.files:
        return "No image in request.files"



    # if file.filename == "":
    #     return "Please select an image to upload"

    # if file:
    #     file.filename = secure_filename(file.filename)
    #     output = upload_file_to_s3(file)
    #     return str(output) ##should be url

    #data = request.json

# call to AWS api - get image link




def upload_file_to_s3(file):

    # with open(file, 'rb') as data:
    #     s3.upload_fileobj(data, BUCKET_NAME, file.key)

    print("inside upload helper function, rile ----> ", file)
    try:
        s3.upload_fileobj(
            file,
            BUCKET_NAME,
            file.key,
        )
    except Exception as e:
        # if s3 upload fails
        return {"errors": str(e)}

    return  f"{S3_BASE_URL}{file.key}"





# def allowed_file(filename):
#     ''' Confirm uploaded image is correct file type.
#     Accepts only JPG or JPEG files, and rejects others. Returns true/false
#     '''
#     return ('.' in filename
#             and filename.rsplit('.', 1)[1].tolower()
#             in ALLOWED_EXTENSIONS)


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
