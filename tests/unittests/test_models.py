from flaskblog import models
import pytest
from sqlalchemy.exc import IntegrityError
from datetime import datetime


@pytest.mark.parametrize('database, username, email, image_file, password', [
    (None, 'test_user', 'test_user@demo.com', None, 'test_password'),
    (None, 'test_user', 'test_user@demo.com', 'my_image.jpg', 'test_password')
], indirect=['database'], ids=['w_default_image', 'w_explicit_image'])
def test_create_user(database, username, email, image_file, password):
    if image_file is None:
        user = models.User(username=username, email=email, password=password)
    else:
        user = models.User(username=username, email=email,
                           image_file=image_file, password=password)

    database.session.add(user)
    database.session.commit()

    assert models.User.query.count() == 1
    assert models.User.query.first() == user


@pytest.mark.parametrize('database, username, email, password', [
    (None, None, 'test_user@demo.com', 'test_password'),
    (None, 'test_user', None, 'test_password'),
    (None, 'test_user', 'test_user@demo.com', None)
], indirect=['database'], ids=['null_username', 'null_email', 'null_password'])
def test_create_user_fail(database, username, email, password):
    user = models.User(username=username, email=email, password=password)
    database.session.add(user)

    with pytest.raises(IntegrityError):
        database.session.commit()


def test_create_duplicate_user(database):
    user1 = models.User(id=1, username='test_user1', email='test_email', password='test_password')
    user2 = models.User(id=1, username='test_user2', email='test_email', password='test_password')
    database.session.add(user1)
    database.session.add(user2)

    with pytest.raises(IntegrityError):
        database.session.commit()


@pytest.mark.parametrize('database, user1, title, date_posted, content', [
    (None, None, 'test_post', None, 'test_content'),
    (None, None, 'test_post', datetime.utcnow(), 'test_content')
], indirect=['database', 'user1'], ids=['w_current_time', 'w_given_time'])
def test_create_post(database, user1, title, date_posted, content):
    post = models.Post(title=title, content=content, date_posted=date_posted, author=user1)

    database.session.add(post)
    database.session.commit()

    queried_post = models.Post.query.first()
    assert queried_post == post
    assert queried_post.user_id == user1.id
    assert models.Post.query.count() == 1


@pytest.mark.parametrize('database, user1, title, date_posted, content', [
    (None, None, None, None, 'test_content'),
    (None, None, 'test_post', datetime.utcnow(), None)
], indirect=['database', 'user1'], ids=['w_current_time', 'w_given_time'])
def test_create_post_fail(database, user1, title, date_posted, content):
    post = models.Post(title=title, content=content, date_posted=date_posted, author=user1)
    database.session.add(post)

    with pytest.raises(IntegrityError):
        database.session.commit()


def test_create_post_no_author(database):
    post = models.Post(title='test_title', content='test_content')
    database.session.add(post)

    with pytest.raises(IntegrityError):
        database.session.commit()


def test_create_post_duplicate(database):
    post1 = models.Post(id=1, title='test_title1', content='test_content')
    post2 = models.Post(id=2, title='test_title1', content='test_content')
    database.session.add(post1)
    database.session.add(post2)

    with pytest.raises(IntegrityError):
        database.session.commit()


def test_load_user(loaded_database, user1):
    assert user1 == models.load_user(1)
