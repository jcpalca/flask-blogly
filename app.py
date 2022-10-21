"""Blogly application."""
from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
# app.config['SQLALCHEMY_DATABASE_URI'] = (
#   'postgresql://otherjoel:hello@13.57.9.123/otherjoel')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

################################################################################
################### USER ROUTES ################################################
################################################################################

@app.get("/")
def redirect_to_users():
    """Redirect to list of users."""

    return redirect("/users")


@app.get("/users")
def users_page():
    """Show all users."""

    users = User.query.all()

    return render_template("user_list.html", users=users)


@app.get("/users/new")
def new_form_page():
    """Show an add form for users."""

    return render_template("new_form.html")


@app.post("/users/new")
def add_new_form():
    """Process the add form, adding a new user and going back to /users"""

    new_user = User(
        first_name=request.form["first_name"] or None,
        last_name=request.form["last_name"] or None,
        image_url=request.form["image_url"] or None)  # NULL for image url.
    # Image url is empty string if not provided.
    # Want to trigger default option (DEFAULT IMG URL)

    if new_user.first_name == None or new_user.last_name == None:
        flash("Please enter a valid first and last name.")
        return redirect("/users/new")

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.get("/users/<int:user_id>")
def show_user_info(user_id):
    """Show information about the given user."""

    user = User.query.get_or_404(user_id)
    posts = user.posts

    return render_template("user_detail.html", user=user, posts=posts)


@app.get("/users/<int:user_id>/edit")
def show_edit_user(user_id):
    """Show the edit page for a user."""

    user = User.query.get_or_404(user_id)

    return render_template("edit_user.html", user=user)


@app.post("/users/<int:user_id>/edit")
def process_edit_user(user_id):
    """Process the edit form and return user to the /users page."""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"]
    # If no image then get an empty string.

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.post("/users/<int:user_id>/delete")
def delete_user(user_id):
    """Delete the user."""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

################################################################################
################### POST ROUTES ################################################
################################################################################

@app.get("/users/<int:user_id>/posts/new")
def show_post_page(user_id):
    """Show form to add a post for that user"""

    user = User.query.get_or_404(user_id)

    return render_template("post_form.html", user=user)

@app.post("/users/<int:user_id>/posts/new")
def add_new_post(user_id):
    """Handle add form; add post and redirect to the user detail page."""

    user = User.query.get_or_404(user_id)
    new_post = Post(
        title=request.form["title"] or None,
        content=request.form["content"] or None,
        created_at= None,
        user_id = user.id)

    if new_post.title == None or new_post.content == None:
        flash("Please enter a valid title and content.")
        return redirect(f"/users/{user.id}/posts/new")

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user.id}")

@app.get("/posts/<int:post_id>")
def show_post_info(post_id):
    """Show information about the given post."""

    post = Post.query.get_or_404(post_id)
    user = post.user

    return render_template("post_detail.html", post=post, user=user)

@app.get("/posts/<int:post_id>/edit")
def show_edit_post(post_id):
    """Show the edit page for a post."""

    post = Post.query.get_or_404(post_id)

    return render_template("edit_post.html", post=post)

@app.post("/posts/<int:post_id>/edit")
def process_edit_post(post_id):
    """Process the edit form and return user to the post view."""

    post = Post.query.get_or_404(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]

    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post.id}")

@app.post("/posts/<int:post_id>/delete")
def delete_post(post_id):
    """Delete the post."""

    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")
