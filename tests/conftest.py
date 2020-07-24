import pytest
import json
import os
from flaskblog import create_app, db as _db, models, bcrypt
from copy import deepcopy

TEST_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
TEST_USERS_FILE = os.path.join(TEST_DATA_DIR, 'users.json')
TEST_POSTS_FILE = os.path.join(TEST_DATA_DIR, 'posts.json')


def load_users():
    """
    Loads the users into memory to avoid opening file each time a test is run.
    """

    _users = {}
    with open(TEST_USERS_FILE, 'r') as file:
        for i, doc in enumerate(json.load(file)):
            _users[f'user{i}'] = models.User(**doc)

    return _users


__USERS = load_users()


# Modified from http://alexmic.net/flask-sqlalchemy-pytest/
@pytest.fixture(scope='session')
def app():
    """
    Session scoped fixture that sets up the testing app context and yields the app object. After the testing session is
    over, the app context is popped off the stack.
    """

    test_config = os.environ.get('MY_FLASK_APP_CONFIG', 'sqlite_test')
    if 'test' not in test_config:
        pytest.exit(f'Must supply a testing configuration! Supplied config - {test_config}', 1)

    _app = create_app(test_config)

    context = _app.app_context()
    context.push()

    yield _app

    context.pop()


@pytest.fixture(scope='function')
def client(app):
    """
    Opens a test_client context and yields the client. If using this fixture with the req fixture, this one must come
    after the req fixture in the parameter list.
    """

    with app.test_client() as _client:
        yield _client


@pytest.fixture(scope='function')
def req(app):
    """
    Opens a test_request_context and yields it. If using this fixture and client, the request must come before the
    client in the argument list.
    """

    with app.test_request_context() as _request:
        yield _request


# Modified from http://alexmic.net/flask-sqlalchemy-pytest/
@pytest.fixture(scope='session')
def db(app):
    """
    Session scoped fixture that assigns the app to the database, creates the tables, yields the database object, and
    drops all tables once the testing session is complete.
    """

    _db.app = app
    _db.create_all()

    yield _db

    _db.drop_all()


# Modified from http://alexmic.net/flask-sqlalchemy-pytest/
@pytest.fixture(scope='function')
def session(db):
    """
    Function scoped fixture that creates a database session with which tests can independently work in and have no
    effect on other tests as any changes made during this session are rolled backed afterwards.
    """

    connection = db.engine.connect()
    transaction = connection.begin()

    _session = db.create_scoped_session(options={'bind': connection, 'binds': {}})

    db.session = _session

    yield _session

    transaction.rollback()
    connection.close()
    _session.remove()


@pytest.fixture(scope='function')
def users():
    """
    Fixture that returns a list of test users.
    """

    return deepcopy(__USERS)


@pytest.fixture(scope='function')
def posts(users):
    """
    Fixture that returns a list of test posts assigned to the test users.
    """

    _posts = {}
    with open(TEST_POSTS_FILE, 'r') as file:
        for i, doc in enumerate(json.load(file)):
            doc['author'] = users[doc['author']]
            _posts[f'post{i}'] = models.Post(**doc)

    return _posts


@pytest.fixture(scope='function')
def user_2posts(users):
    """
    Fixture that returns a test user with 2 posts.
    """

    return users['user0']


@pytest.fixture(scope='function')
def user_1post(users):
    """
    Fixture that returns a test user with 1 post.
    """

    return users['user1']


@pytest.fixture(scope='function')
def user_0post(users):
    """
    Fixture that returns a test user with 0 posts.
    """

    return users['user2']


@pytest.fixture(scope='function')
def post(posts):
    """
    Fixture that returns a test post belonging to test_user0.
    """

    return posts['post0']


@pytest.fixture(scope='function')
def loaded_db(session, users, posts, request):
    """
    Function scoped fixture that returns a session object that has already been preloaded with data. All changes made to
    this session are rolled back after the test.
    """

    for user in users.values():
        if request.__dict__.get('param'):
            user.password = bcrypt.generate_password_hash(user.password).decode('utf-8')
        session.add(user)

    for post in posts.values():
        session.add(post)

    session.commit()

    yield session
