from flask_sqlalchemy import SQLAlchemy
from PIL import Image as Pil_Image
from urllib.request import urlopen
import io
from datetime import datetime

from AWS.AWS import AWS
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

    def __repr__(self):
        rep = 'Image(' + str(self.id) + ',' + str(self.file_name) + ')'
        return rep

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

        print(f' -----> BACKEND API - SQL -----> Image added to Database')

        db.session.add(image)

        return image

    @classmethod
    def update(cls, file_name, data, bucket_name):
        ''' Method for updating an image
                updates database, and uploads to s3. '''

        image = cls.query.filter_by(file_name=file_name).first()
        return image

    @classmethod
    def fetch_binary_img(cls, file_name, bucket_name):
        ''' Call to AWS API, retrieve binary data. return binary '''
        s3_object = AWS.get_object(file_name, bucket_name)
        img_content = s3_object['Body'].ready()
        return img_content

    def serialize(self):
        ''' serialize self for JSON response '''

        return {
            "url": self.image_url,
            "first_name": self.file_name,
            "title": self.title,
            "description": self.description,
            "creation_date": self.creation_date
        }

        ###### PILLOW METHODS ######

        # Reading from URL
        # from PIL import Image as Pil_Image
        # from urllib.request import urlopen

        # url = "https://python-pillow.org/images/pillow-logo.png"
        # img = Pil_Image.open(urlopen(url))

        # Reading from binary data
        # from PIL import Pil_Image
        # import io

        # im = Image.open(io.BytesIO(buffer))

    def rotate(self, degrees=45):
        ''' Used to rotate an image , clockwise'''
        print('rotate()-> received', self, 'degrees: ', degrees)

    def bw(self):
        ''' Used to change an image to black and white '''
        print(' bw() -> received', self)

    def sepia(self):
        ''' Used to change an image to sepia '''
        print('sepia() -> received', self)

    def add_border(self, pixels, color):
        ''' Used to add a border to an image'''
        print('add_border() -> received', self)

    def change_size(self, height, width, lock_ratio=True):
        ''' Used to change size of image'''
        print('reduce_size() -> received', self)
