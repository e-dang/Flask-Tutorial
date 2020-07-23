from flaskblog import models
import pytest
from sqlalchemy.exc import IntegrityError
from datetime import datetime


@pytest.mark.parametrize('session, username, email, image_file, password', [
    (None, 'test_user', 'test_user@demo.com', None, 'test_password'),
    (None, 'test_user', 'test_user@demo.com', 'my_image.jpg', 'test_password')
], indirect=['session'], ids=['w_default_image', 'w_explicit_image'])
def test_create_user(session, username, email, image_file, password):
    if image_file is None:
        user = models.User(username=username, email=email, password=password)
    else:
        user = models.User(username=username, email=email,
                           image_file=image_file, password=password)

    session.add(user)
    session.commit()

    assert models.User.query.count() == 1
    assert models.User.query.first() == user


@pytest.mark.parametrize('session, username, email, password', [
    (None, None, 'test_user@demo.com', 'test_password'),
    (None, 'test_user', None, 'test_password'),
    (None, 'test_user', 'test_user@demo.com', None)
], indirect=['session'], ids=['null_username', 'null_email', 'null_password'])
def test_create_user_fail(session, username, email, password):
    user = models.User(username=username, email=email, password=password)
    session.add(user)

    with pytest.raises(IntegrityError):
        session.commit()


def test_create_duplicate_user(session):
    user1 = models.User(id=1, username='test_user1', email='test_email', password='test_password')
    user2 = models.User(id=1, username='test_user2', email='test_email', password='test_password')
    session.add(user1)
    session.add(user2)

    with pytest.raises(IntegrityError):
        session.commit()


@pytest.mark.parametrize('session, user_0post, title, date_posted, content', [
    (None, None, 'test_post', None, 'test_content'),
    (None, None, 'test_post', datetime.utcnow(), 'test_content')
], indirect=['session', 'user_0post'], ids=['w_current_time', 'w_given_time'])
def test_create_post(session, user_0post, title, date_posted, content):
    post = models.Post(title=title, content=content, date_posted=date_posted, author=user_0post)

    session.add(post)
    session.commit()

    queried_post = models.Post.query.first()
    assert queried_post == post
    assert queried_post.user_id == user_0post.id
    assert models.Post.query.count() == 1


@pytest.mark.parametrize('session, user_0post, title, date_posted, content', [
    (None, None, None, None, 'test_content'),
    (None, None, 'test_post', datetime.utcnow(), None)
], indirect=['session', 'user_0post'], ids=['w_current_time', 'w_given_time'])
def test_create_post_fail(session, user_0post, title, date_posted, content):
    post = models.Post(title=title, content=content, date_posted=date_posted, author=user_0post)
    session.add(post)

    with pytest.raises(IntegrityError):
        session.commit()


def test_create_post_no_author(session):
    post = models.Post(title='test_title', content='test_content')
    session.add(post)

    with pytest.raises(IntegrityError):
        session.commit()


def test_create_post_duplicate(session):
    post1 = models.Post(id=1, title='test_title1', content='test_content')
    post2 = models.Post(id=2, title='test_title1', content='test_content')
    session.add(post1)
    session.add(post2)

    with pytest.raises(IntegrityError):
        session.commit()


def test_load_user(loaded_db, users):
    for i, user in enumerate(users.values(), start=1):
        assert user == models.load_user(i)
