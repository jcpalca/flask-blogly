from unittest import TestCase

from app import app, db
from models import DEFAULT_IMG_URL, User, connect_db

# Let's configure our app to use a different database for tests
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly_test"
# app.config['SQLALCHEMY_DATABASE_URI'] = (
#     "postgresql://otherjoel:hello@13.57.9.123/otherjoel_test")

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

connect_db(app)
db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        User.query.delete()

        self.client = app.test_client()

        test_user = User(
            first_name="test_first",
            last_name="test_last",
            image_url=None,
        )

        second_user = User(
            first_name="test_first_two",
            last_name="test_last_two",
            image_url=None,
        )

        db.session.add_all([test_user, second_user])
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_list_users(self):
        """Test if users list page html appears."""
        with self.client as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test_first", html)
            self.assertIn("test_last", html)

    def test_users_redirection(self):
        """Test redirect from root to users page."""
        with self.client as c:
            resp = c.get("/")
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "/users")

    def test_users_redirection_followed(self):
        """Test if users page reached after redirection."""
        with self.client as c:
            resp = c.get("/", follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("test_first", html)
            self.assertIn("test_last", html)

    def test_get_add_user(self):
        """Test if new user form page is rendered with html."""
        with self.client as c:
            resp = c.get("/users/new")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("<h1>Create a user</h1>", html)

    def test_post_add_user(self):
        """Tests if redirection to users page works if data is valid."""
        with self.client as c:
            resp = c.post("/users/new", data={"first_name": "Spencer",
                                              "last_name": "Brit",
                                              "image_url": ''})
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "/users")

    def test_post_add_user_followed(self):
        """Test if users page reached and results show after redirection."""
        with self.client as c:
            resp = c.post("/users/new", data={"first_name": "Spencer",
                                              "last_name": "Brit",
                                              "image_url": ''},
                                              follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Spencer", html)
            self.assertIn("Brit", html)

    def test_post_add_invalid_user(self):
        """Tests if redirection to users page works if data is invalid."""
        with self.client as c:
            resp = c.post("/users/new", data={"first_name": "",
                                              "last_name": "",
                                              "image_url": ''})
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "/users/new")

    def test_post_add_invalid_user_followed(self):
        """Test if users page reached and results show after invalid
        redirection."""

        with self.client as c:
            resp = c.post("/users/new", data={"first_name": "",
                                              "last_name": "",
                                              "image_url": ''},
                                              follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Please enter a valid first and last name", html)

    def test_get_add_post(self):
        """Test if new post form page is rendered with html."""
        with self.client as c:
            user_data = User.query.all()
            test_user = user_data[0]
            resp = c.get(f"/users/{test_user.id}/posts/new")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("Create Post", html)

    def test_post_add_post(self):
        """Tests if redirection to user detail page works if data is valid."""
        with self.client as c:
            user_data = User.query.all()
            test_user = user_data[0]
            resp = c.post(f"/users/{test_user.id}/posts/new",
                            data={"title": "Testing",
                            "content": "This is test content",
                            "created_at": '',
                            "user_id": {test_user.id}})
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, f"/users/{test_user.id}")


