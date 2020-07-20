import pytest
from flaskblog import create_app, db
from flaskblog import models


@pytest.fixture
def app(tmpdir):
    app = create_app('test')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{tmpdir.join("tmpdb.db")}'  # set db to temporary file

    with app.app_context():
        db.create_all()

        yield app


@pytest.fixture
def client(app):
    yield app.test_client()


@pytest.fixture
def database(app):
    yield db


@pytest.fixture
def user1():
    return models.User(username='test_user1', email='test_email1@demo.com', password='test_password1')


@pytest.fixture
def user2():
    return models.User(username='test_user2', email='test_email2@demo.com', password='test_password2')


@pytest.fixture
def user3():
    return models.User(username='test_user3', email='test_email3@demo.com', password='test_password3')


@pytest.fixture
def post1(user1):
    return models.Post(title='test_title1', content='test_content1', author=user1)


@pytest.fixture
def post2(user1):
    return models.Post(title='test_title2', content='test_content2', author=user1)


@pytest.fixture
def post3(user2):
    return models.Post(title='test_title3', content='test_content3', author=user2)


@pytest.fixture
def users(user1, user2, user3):
    return [user1, user2, user3]


@pytest.fixture
def posts(post1, post2, post3):
    return [post1, post2, post3]


@pytest.fixture
def loaded_database(database, users, posts):
    for user in users:
        database.session.add(user)

    for post in posts:
        database.session.add(post)

    database.session.commit()

    yield database
