from flask_sqlalchemy import SQLAlchemy
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
        unique=False
    )

    image_url = db.Column(
        db.Text,
        default=DEFAULT_IMAGE_URL,
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
    def create(cls, file, bucket_name, title=None):
        ''' Method for adding an image.
                Pushes image to database, and uploads to s3.
                returns image object
        '''
        file.key = Image.get_unique_key(file.filename)
        s3_image_url = AWS.upload(file, bucket_name)

        image = Image(
            title=title,
            file_name=file.key,
            image_url=s3_image_url
        )
        print(image)
        print(s3_image_url)

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
