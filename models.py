from flask_sqlalchemy import SQLAlchemy
from PIL import Image as PIL
from PIL.ExifTags import TAGS
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
ALLOWED_EXTENSIONS = {"jpg", "jpeg"}


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

    # An images metadata can be accessed with img.img_metadata
    img_metadata = db.relationship('Img_Metadata', backref="image")

    @ classmethod
    def allowed_file(cls, filename):
        ''' TODO:'''
        return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

    @ classmethod
    def get_unique_key(cls):
        ''' TODO:'''
        uuid_key = uuid.uuid4().hex
        return uuid_key

    # Extracts file type from image name and returns it
    @classmethod
    def get_file_type(cls, filename):
        '''TODO:'''
        return "." in filename and \
            filename.rsplit(".", 1)[1].lower()

    @classmethod
    def create(cls, file, bucket_name, title=None, description=None):
        ''' Method for adding an image.
                Pushes image to database, and uploads to s3.
                returns image object
                TODO:
        '''

        id = Image.get_unique_key()
        ext = Image.get_file_type(file.filename)
        file_name = f'{id}.{ext}'
        image_url = AWS.object_url(bucket_name, file_name)

        # Add Image to DB.
        try:
            image: Image = Image(
                id=id,
                ext=ext,
                title=title,
                file_name=file_name,
                image_url=image_url,
                bucket_name=bucket_name,
                description=description,
            )

            # parse metadata, add to db FIXME: fix - file IO issues
            md = cls.fetch_metadata(file)
            for k, v in md:
                metadata = Img_Metadata(
                    tag_name=k,
                    value=v
                )
                image.img_metadata.append(metadata)

        except TypeError as error:
            print(error)
            return {"errors": str(error)}

        # After adding to DB, upload to AWS S3
        try:
            file.seek(0)
            AWS.upload(file, bucket_name, file_name, ext=ext)
        except ValueError as error:
            print(error)
            return {"errors": str(error)}

        db.session.add(image)

        print(f' -----> BACKEND API - SQL -----> Image added to Database')
        return id

    @ classmethod
    def fetch_binary_img(cls, file_name, bucket_name):
        ''' Call to AWS API, retrieve binary data. return binary
        TODO:'''
        s3_object = AWS.get_object(file_name, bucket_name)
        img_content = s3_object['Body'].ready()
        return img_content

    def update(self, pil_img, updated_img):
        ''' Method for updating image content.

        Accepts a file, uploads it to S3 under same key.
        Returns True / False
        TODO:
        '''

        try:
            in_mem_file = io.BytesIO()
            updated_img.save(in_mem_file, format=pil_img.format)
            in_mem_file.seek(0)
            print(in_mem_file)

        except BufferError as error:
            print(error)
            return {"errors": str(error)}

        try:
            AWS.upload(in_mem_file, self.bucket_name,
                       file_name=self.file_name,
                       ext=self.ext)
        except ValueError as error:
            print(error)
            return {"errors": str(error)}

        return True

    @ classmethod
    def fetch_metadata(cls, file):
        ''' Extract metadata of an image from request
        TODO:'''
        breakpoint

        meta = []
        with PIL.open(file) as pil_img:
            exifdata = pil_img.getexif()
            for tagid in exifdata:
                tagname = TAGS.get(tagid, tagid)
                value = str(exifdata.get(tagid))
                meta.append((tagname, value))
            pil_img.seek(0)

        return meta

    def serialize(self):
        ''' serialize self for JSON response
        TODO:'''
        print('serializing response')

        return {
            "url": self.image_url,
            "file_name": self.file_name,
            "ext": self.ext,
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "creation_date": self.creation_date,
            "metadata": 'not available yet'
        }

################################ PILLOW METHODS ###############################

        # These are methods for transforming an image, using the Pillow library.
        # Reading from URL
        # from PIL import Image as PIL
        # from urllib.request import urlopen

        # url = "https://python-pillow.org/images/pillow-logo.png"
        # img = PIL.open(urlopen(url))

        # Reading from binary data
        # from PIL import Pil_Image
        # import io

        # im = Image.open(io.BytesIO(buffer))

    def fetch_from_url(self):
        ''' Fetch image content from AWS
        TODO: '''
        pil_image = PIL.open(urlopen(self.image_url))
        return pil_image

        # def bw(self): TODO:
        #     ''' Used to change an image to black and white '''
        #     print(' bw() -> received', self)

        # def sepia(self): TODO:
        #     ''' Used to change an image to sepia '''
        #     print('sepia() -> received', self)

        # def add_border(self, pixels, color): TODO:
        #     ''' Used to add a border to an image'''
        #     print('add_border() -> received', self)

        # def change_size(self, height, width, lock_ratio=True): TODO:
        #     ''' Used to change size of image'''
        #     print('reduce_size() -> received', self)


################################ Img_Metadata ###############################

class Img_Metadata(db.Model):
    """A piece of image metadata TODO:"""

    __tablename__ = 'img_metadata'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    tag_name = db.Column(
        db.String(50),
        nullable=False,
    )
    value = db.Column(
        db.String(200),
        nullable=False,
    )

    file_id = db.Column(
        db.Text,
        db.ForeignKey('images.id', ondelete='CASCADE'),
        nullable=False,
    )

    def __repr__(self):
        return f"<Metadata #{self.id}: Tag Name {self.tag_name} Value {self.value} Image {self.file_id}>"
