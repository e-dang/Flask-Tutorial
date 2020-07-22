import pytest
import json
import os
from flaskblog import create_app, db as _db
from flaskblog import models
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
def app(tmp_path_factory):
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{tmp_path_factory.mktemp("flaskblog") / "tmpdb.db"}'
    _app = create_app('test', SQLALCHEMY_DATABASE_URI=SQLALCHEMY_DATABASE_URI)

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
    _db.app = app
    _db.create_all()

    yield _db

    _db.drop_all()


# Modified from http://alexmic.net/flask-sqlalchemy-pytest/
@pytest.fixture(scope='function')
def session(db):
    connection = db.engine.connect()
    transaction = connection.begin()

    _session = db.create_scoped_session(options={'bind': connection, 'binds': {}})

    db.session = _session

    yield _session

    transaction.rollback()
    connection.close()
    _session.remove()


@pytest.fixture(scope='function')
def tmp_db(db):
    """
    Fixture for when the database tables need to be filled, dropped, and reset and session fixture doesn't work.
    """
    connection = db.engine.connect()
    _session = db.create_scoped_session(options={'bind': connection, 'binds': {}})
    db.session = _session

    yield db

    connection.close()
    db.drop_all()
    db.create_all()


@pytest.fixture(scope='function')
def users():
    return deepcopy(__USERS)


@pytest.fixture(scope='function')
def posts(users):
    _posts = {}
    with open(TEST_POSTS_FILE, 'r') as file:
        for i, doc in enumerate(json.load(file)):
            doc['author'] = users[doc['author']]
            _posts[f'post{i}'] = models.Post(**doc)

    return _posts


@pytest.fixture(scope='function')
def user_2posts(users):
    return users['user0']


@pytest.fixture(scope='function')
def user_1post(users):
    return users['user1']


@pytest.fixture(scope='function')
def user_0post(users):
    return users['user2']


@pytest.fixture(scope='function')
def loaded_db(tmp_db, users, posts):
    for user in users.values():
        tmp_db.session.add(user)

    for post in posts.values():
        tmp_db.session.add(post)

    tmp_db.session.commit()

    yield tmp_db
