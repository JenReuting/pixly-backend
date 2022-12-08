from models import (
    db, connect_db, Image
)
from flask_debugtoolbar import DebugToolbarExtension

import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from AWS.AWS import AWS

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

############################# Before All Requests ################################


@app.before_request
def log_request():
    """Confirms receipt of request, and anything passed to it. """

    print(
        f' -----> BACKEND API - INCOMING REQUEST -----> {request}')


############################# Image Upload ################################

@ app.route('/upload', methods=["POST"])
def upload_image():
    """ Handle image upload. Adds image and returns data about new image.
    """

    file = request.files.get('image') or None
    title = request.form.get('title') or None
    description = request.form.get('description') or None

    print(
        f' -----> BACKEND API - POST /upload -----> file: {file} title: {title} description: {description}')

    if not file:
        return {'error': 'Provide a valid image'}

    try:
        image = Image.create(file, BUCKET_NAME, title, description)

    except ValueError as e:
        print(e)

    db.session.commit()

    print(
        f' -----> BACKEND API - OUTGOING RESPONSE ----->  image created: {image}')

    return {"url": image.image_url,
            'file_name': image.file_name,
            'title': image.title,
            'description': image.description,
            'creation_date': image.creation_date}


############################# Image Download ################################

@ app.route('/images/', methods=['GET'])
def get_image_data():
    ''' Returns data for a single image.
            Params: file_name like: 'file_name.jpg'
            Returns:
                Image like:
                    {url, file_name, title, description, creation_date}
    '''

    file_name = request.args.get('file_name') or None

    # Return all images
    if not file_name:
        print(
            f' -----> BACKEND API - GET /:file_name -----> all images:')
        images = Image.query.all()
        serialized = [i.serialize() for i in images]
        return jsonify(images=serialized)

    # Return image by file_name
    else:
        print(
            f' -----> BACKEND API - GET /:file_name -----> file_name: {file_name}')
        image = Image.query.filter(
            Image.file_name.like(f"%{file_name}%")).first()

        serialized = image.serialize()
        return jsonify(image=serialized)


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
