from flask_sqlalchemy import SQLAlchemy
import uuid

db = SQLAlchemy()

DEFAULT_IMAGE_URL = './default.jpg'


class Image(db.model):
    """
    --
    """

    __tablename__ = 'images'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)

    filename = db.Column(
            db.Text,
            nullable=False,
            unique=False
        )

    image_url = db.Column(
        db.Text,
        default=DEFAULT_IMAGE_URL,
    )

    filename = db.Column(
        db.Text,
        nullable=False,
        unique=False
    )

    image_url = db.Column(
        db.Text,
        default=DEFAULT_IMAGE_URL,
    )

    ########## helper functions ###############

    ALLOWED_EXTENSIONS={"jpg", "jpeg", "gif", "png"}

    def allowed_file(filename):
        return "." in filename and \
            filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

    def get_unique_key(filename):
        ext = filename.rsplit(".", 1)[1].lower()
        uuid_key = uuid.uuid4().hex
        return f"{uuid_key}.{ext}"



def connect_db(app):
    """ Connect to database. """

    app.app_context().push()
    db.app = app
    db.init_app(app)

