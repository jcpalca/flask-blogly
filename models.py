"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMG_URL = (
"https://cdn.pixabay.com/photo/2022/10/05/20/43/hyacinth-macaw-7501470__340.jpg"
)

def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User."""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    first_name = db.Column(db.String(50),
                           nullable = False)
    last_name = db.Column(db.String(50),
                          nullable = False)
    image_url = db.Column(db.String(100),
                          nullable = False,
                          default = DEFAULT_IMG_URL)
