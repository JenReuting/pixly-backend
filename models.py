from flask_sqlalchemy import SQLAlchemy
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
    --
    """

    __tablename__ = 'images'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)

    file_name = db.Column(
        db.Text,
        nullable=False,
        unique=False
    )

    image_url = db.Column(
        db.Text,
        default=DEFAULT_IMAGE_URL,
    )

    ########## helper functions ###############

    @classmethod
    def allowed_file(filename):
        return "." in filename and \
            filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

    @classmethod
    def get_unique_key(filename):
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
            file_name=file.key,
            image_url=s3_image_url
        )

        db.session.add(image)
        return image
