"""Blogly application."""

from flask import Flask, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

connect_db(app)
db.drop_all()
db.create_all()


@app.get("/")
def redirect_to_users():
    """Redirect to list of users."""

    return redirect("/users")


@app.get("/users")
def users_page():
    """Show all users."""

    users = db.session.query(
        User.first_name, User.last_name
    ).all()

    return render_template("user_list.html", users=users)


@app.get("/users/new")
def new_form_page():
    """Show an add form for users."""

    return render_template("new_form.html")


@app.post("/users/new")
def add_new_form():
    """Process the add form, adding a new user and going back to /users"""

    new_user = User(
        first_name = request.form()
    )
    return redirect("/users")


@app.get("/users/<int:user_id>")
def show_user_info(user_id):
    """Show information about the given user."""

    return render_template("user_detail.html")


@app.get("/users/<int:user_id>/edit")
def show_edit_page(user_id):
    """Show the edit page for a user."""

    return render_template("edit_user.html")


@app.post("/users/<int:user_id>/edit")
def process_edit_form(user_id):
    """Process the edit form and return user to the /users page."""

    return redirect("/users")


@app.post("/users/<int:user_id>/delete")
def delete_user_page(user_id):
    """Delete the user."""

    return redirect("/users")
