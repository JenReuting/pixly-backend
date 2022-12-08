from models import (
    db, connect_db, Image
)
from flask_debugtoolbar import DebugToolbarExtension

import os
from dotenv import load_dotenv
from flask import Flask, request
from flask_cors import CORS
from AWS import AWS

app = Flask(__name__)
CORS(app)

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
    file = request.files['image']
    print('image from route', file)

    # NOTE: request.form gives us the other data in the multipart request (ex: request.form['filename'])

    try:
        image = Image.create(file, BUCKET_NAME)
        print('Successfully created image', image)
    except ValueError as e:
        print(e)

    db.session.commit()
    print("image from upload image -----> ", image.image_url)
    print("image from upload imag, file_name -----> ", image.file_name)
    print("image from upload image ----->,  title", image.title)
    return {"url": image.image_url}



############################## Image Modification ###########################
