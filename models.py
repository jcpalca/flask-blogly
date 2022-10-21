"""Models for Blogly."""
import datetime
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

    posts = db.relationship("Post", backref="user")

class Post(db.Model):
    """Post."""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    title = db.Column(db.String(25),
                      nullable = False,
                      unique = True)
    content = db.Column(db.String(1600),
                        nullable = False)
    created_at = db.Column(db.DateTime,
                        nullable = False,
                        default = datetime.datetime.now),
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable = False)
