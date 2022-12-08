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

    file = request.files.get('image') or None
    title = request.form.get('title') or None
    description = request.form.get('description') or None

    print(
        f' -----> BACKEND API - POST /upload received: file: {file} title: {title} description: {description}')

    if not file:
        return {'error': 'Provide a valid image'}

    try:
        image = Image.create(file, BUCKET_NAME, title, description)
        print('Successfully created image', image)
    except ValueError as e:
        print(e)

    db.session.commit()

    return {"url": image.image_url,
            'file_name': image.file_name,
            'title': image.title,
            'description': image.description,
            'creation_date': image.creation_date}


##############################################################################
# Turn off all caching in Flask
#   (useful for dev; in production, this kind of stuff is typically
#   handled elsewhere)
#
# https://stackoverflow.com/questions/34066804/disabling-caching-in-flask

@ app.after_request
def add_header(response):
    """Add non-caching headers on every request."""

    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control
    response.cache_control.no_store = True
    return response
