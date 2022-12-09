from flask_sqlalchemy import SQLAlchemy
from PIL import Image as Pil_Image
from urllib.request import urlopen
import io
from datetime import datetime
from botocore.exceptions import ClientError


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
        rep = f'Image(id: {str(self.id)}, file_name: {str(self.file_name)}, bucket_name: {str(self.bucket_name)})'
        return rep

    id = db.Column(
        db.Text,
        primary_key=True)

    ext = db.Column(
        db.Text,
        nullable=False,
        unique=False
    )

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

    @ classmethod
    def allowed_file(cls, filename):
        ''' '''
        return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

    @ classmethod
    def get_unique_key(cls):
        ''' '''
        uuid_key = uuid.uuid4().hex
        return uuid_key

    # Extracts file type from image name and returns it
    @classmethod
    def get_file_type(cls, filename):
        return "." in filename and \
            filename.rsplit(".", 1)[1].lower()

    @classmethod
    def create(cls, file, bucket_name, title=None, description=None):
        ''' Method for adding an image.
                Pushes image to database, and uploads to s3.
                returns image object
        '''

        id = Image.get_unique_key()
        ext = Image.get_file_type(file.filename)
        file_name = f'{id}.{ext}'
        image_url = AWS.object_url(bucket_name, file_name)

        # Add Image to DB
        try:
            image = Image(
                id=id,
                ext=ext,
                title=title,
                file_name=file_name,
                image_url=image_url,
                bucket_name=bucket_name,
                description=description,
            )
        except TypeError as e:
            print(e)

            # Add image to AWS S3
        try:
            AWS.upload(file, bucket_name, file_name=file_name, extension=ext)
        except ValueError as e:
            print(e)

        db.session.add(image)

        print(f' -----> BACKEND API - SQL -----> Image added to Database')
        return image

    @classmethod
    def fetch_binary_img(cls, file_name, bucket_name):
        ''' Call to AWS API, retrieve binary data. return binary '''
        s3_object = AWS.get_object(file_name, bucket_name)
        img_content = s3_object['Body'].ready()
        return img_content

    def update(self, pil_img, updated_img):
        ''' Method for updating image content.

        Accepts a file, uploads it to S3 under same key.
        Returns Image
        '''

        try:
            in_mem_file = io.BytesIO()
            updated_img.save(in_mem_file, format=pil_img.format)
            in_mem_file.seek(0)
        except BufferError as e:
            print(e)

        try:
            AWS.upload(in_mem_file, self.bucket_name,
                       file_name=self.file_name,
                       extension=self.ext)
        except ValueError as e:
            print(e)

    def serialize(self):
        ''' serialize self for JSON response '''

        return {
            "url": self.image_url,
            "file_name": self.file_name,
            "ext": self.ext,
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "creation_date": self.creation_date,
            "metadata": {
                'camera': 'nikon',
                'location': 'san francisco'
            }
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

    # @classmet

    def fetch_from_url(self):
        ''' Fetch image content from AWS '''
        pil_image = Pil_Image.open(urlopen(self.image_url))
        return pil_image

    # def extract_metadata():

    # def bw(self):
    #     ''' Used to change an image to black and white '''
    #     print(' bw() -> received', self)

    # def sepia(self):
    #     ''' Used to change an image to sepia '''
    #     print('sepia() -> received', self)

    # def add_border(self, pixels, color):
    #     ''' Used to add a border to an image'''
    #     print('add_border() -> received', self)

    # def change_size(self, height, width, lock_ratio=True):
    #     ''' Used to change size of image'''
    #     print('reduce_size() -> received', self)
