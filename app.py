from models import (
    db, connect_db, Image
)
# from flask_debugtoolbar import DebugToolbarExtension

import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
import helpers


app = Flask(__name__)
CORS(app)


load_dotenv()

############ DB IMPORT CONFIG ###########################

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ['DATABASE_URL'].replace("postgres://", "postgresql://"))
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
connect_db(app)


# toolbar = DebugToolbarExtension(app)


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

############################# All Requests ################################


@app.route('/', methods=['GET'])
def home():
    """ Handle routes to homepage. """

    message = {
        'PIXLY': 'Welcome to Pixly',
        'routes': {
            'fetch_all_images': {
                'help_text': 'Returns data for all images in DB.',
                'method': 'GET',
                'route': '/images',
                'returns': '''{Images: [{id, ext, url, file_name, title, description, creation_date}...]''',
            },
            'fetch_image_by_id': {
                'help_text': 'Returns image data for a single image by ID',
                'method': 'GET',
                'route': '/images/<id>',
                'returns': '''{Image:{id, ext, url, file_name, title, description, creation_date}''',
            },
            'update_image': {
                'help_text': 'Updates image data for a single image by ID',
                'method': 'PATCH',
                'route': '/images/<id>',
                'params': "changes : {'bw'}",
                'returns': '''{Image:{id, ext, url, file_name, title, description, creation_date}''',
            },
            'delete_image': {
                'help_text': 'Deletes image data for a single image by ID',
                'method': 'DELETE',
                'route': '/images/<id>',
                'returns': '''Image deleted <id> ''',
            }

        }
    }

    return jsonify(message)


############################# Image Upload ################################

@app.route('/upload', methods=["POST"])
def upload_image():
    """ Handle image upload. Adds image and returns data about new image.
    TODO: """

    file = request.files.get('image') or None
    title = request.form.get('title') or None
    description = request.form.get('description') or None

    print(
        f' -----> BACKEND API - POST /upload -----> file: {file} title: {title} description: {description}')

    if not file:
        return {'error': 'Provide a valid image'}

    try:
        id = Image.create(file, BUCKET_NAME, title, description)
        image = Image.query.get_or_404(id)
        serialized = image.serialize()

    except ValueError as e:
        print(e)

    db.session.commit()

    print(
        f' -----> BACKEND API - OUTGOING RESPONSE ----->  image created: {image}')

    return jsonify(image=serialized)


############################# Image Download ################################

@ app.route('/images/', methods=['GET'])
def get_all_images():
    ''' TODO:Returns data for ALL images.
            Params:
                limit: number of items to return, (indexes)
            Returns:
                {Images:
                    [{id, ext, url, file_name, title, description, creation_date}...]
    '''
    try:
        images = Image.query.all()  # add limit, return
    except ValueError as e:
        print(e)

    serialized = [i.serialize() for i in images]

    return jsonify(images=serialized)


@ app.route('/images/<id>', methods=['GET'])
def get_image(id):
    ''' TODO:Returns data for a single image.
            Params:
                file_name like: 'file_name.jpg'
                limit: number of items to return, (indexes)

            Returns:
                Image like:
                    {url, file_name, title, description, creation_date}
    '''

    print(
        f' -----> BACKEND API - GET /:file_name -----> id: {id}')
    try:
        image = Image.query.get_or_404(id)

    except ValueError as e:
        print(e)

    serialized = image.serialize()
    return jsonify(image=serialized)


############################# Image Update ################################


@app.route('/images/<id>', methods=['PATCH'])
def update_image(id):
    ''' TODO: Handles updates to a specific image.
        Params:
            changes: 'rotate', 'bw', 'sepia'
        Returns:
                Image like:
                    {url, file_name, title, description, creation_date}
    '''
    image = Image.query.get_or_404(id)
    request_json = request.get_json()
    action = request_json.get('change') or None
    # action = request.args.get('changes') or None

    if action:

        print(
            f' -----> BACKEND API - GET /:file_name -----> id: {id}')

        try:
            pil_img = image.fetch_from_url()

            if ('rotate' in action):
                print('yes')
                updated = pil_img.rotate(90)
            elif ('bw' in action):
                updated = pil_img.convert('L')
            elif ('sepia' in action):
                updated = helpers.convert_sepia(pil_img)

            image.update(pil_img, updated)
            serialized = image.serialize()

        except ValueError as error:
            print(error)
            return {"errors": str(error)}

    return jsonify(image=serialized)


@app.route('/images/<id>', methods=['DELETE'])
def delete_image(id):
    ''' TODO: Deletes an image from the database.
        Params:
            id: image id like : 359u50305831058
        Returns:
                Returns 'Image: {id} deleted' on success, else throws error if not found.
'''
    image = Image.query.get_or_404(id)

    try:
        Image.delete_image(image)
    except ValueError as e:
        print(e)

    db.session.commit()

    return jsonify(f'Image: {id} deleted')

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
