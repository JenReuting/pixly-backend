# from sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

# DEFAULT_IMAGE_URL = ''

# class Image(db.model):
#     """
#     --
#      """

#     __tablename__ = 'images'

#     id = db.Column(
#         db.Integer,
#         primary_key=True,
#         autoincrement=True)

#     filename = db.Column(
#         db.Text,
#         nullable=False,
#         unique=False
#     )

#     image_url = db.Column(
#         db.Text,
#         default=DEFAULT_IMAGE_URL,
#     )

# def connect_db(app):
#     """ Connect to database. """

#     app.app_context().push()
#     db.app = app
#     db.init_app(app)