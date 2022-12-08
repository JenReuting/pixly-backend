from flask_sqlalchemy import SQLAlchemy
from PIL import Image as pil
from urllib.request import urlopen
import io
from datetime import datetime

from AWS import AWS
import uuid

db = SQLAlchemy()


def connect_db(app):
    """ Connect to database. """

    app.app_context().push()
    db.app = app
    db.init_app(app)


DEFAULT_IMAGE_URL = './default.jpg'
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "gif", "png"}


class Image(db.Model):
    """
    Image in the system. Loaded to the DB, and to AWS s3.
    """

    __tablename__ = 'images'

    def __new__(cls, *args, **kwargs):
        print("1. Create a new instance of Image.")
        return super().__new__(cls)

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)

    title = db.Column(
        db.Text,
        nullable=True
    )

    file_name = db.Column(
        db.Text,
        nullable=False,
        unique=True
    )

    image_url = db.Column(
        db.Text,
        default=DEFAULT_IMAGE_URL,
    )

    bucket_name = db.Column(
        db.Text,
        nullable=False,
        unique=False
    )

    description = db.Column(
        db.Text,
        nullable=True,
        unique=False
    )

    creation_date = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    @classmethod
    def allowed_file(cls, filename):
        return "." in filename and \
            filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

    @classmethod
    def get_unique_key(cls, filename):
        ext = filename.rsplit(".", 1)[1].lower()
        uuid_key = uuid.uuid4().hex
        return f"{uuid_key}.{ext}"

    @classmethod
    def create(cls, file, bucket_name, title=None, description=None):
        ''' Method for adding an image.
                Pushes image to database, and uploads to s3.
                returns image object
        '''
        file.key = Image.get_unique_key(file.filename)
        s3_image_url = AWS.upload(file, bucket_name)

        image = Image(
            title=title,
            file_name=file.key,
            description=description,
            image_url=s3_image_url,
            bucket_name=bucket_name
        )
        db.session.add(image)
        return image

    @classmethod
    def update(cls, file_name, data, bucket_name):
        ''' Method for updating an image
                updates database, and uploads to s3. '''

        image = cls.query.filter_by(file_name=file_name).first()
        return image

    @classmethod
    def get_all_images(cls):
        ''' Retrieve all images from DB
                Returns array of Images
        '''
        images = cls.query.all()
        return images

    def get_binary_img(file_name, bucket_name):
        ''' Call to AWS API, retrieve binary data. return binary '''
        s3_object = AWS.get_object(file_name, bucket_name)
        img_content = s3_object['Body'].ready()
        return img_content

    # def rotate(image, degrees=90):
    #     ''' Used to rotate an image '''
    #     print('Rotate -> received', image, 'degrees: ', degrees)
