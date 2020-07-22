import pytest
import mock
from flask import request


@mock.patch('flaskblog.posts.routes.db')
def test_new_post_post(mock_db, req, client, post, user_2posts, session):
    with mock.patch('flaskblog.posts.routes.current_user', user_2posts):
        resp = client.post('/post/new', data={'title': post.title,
                                              'content': post.content}, follow_redirects=True)

    mock_db.session.add.assert_called_once()
    mock_db.session.commit.assert_called_once()
    post = mock_db.session.add.call_args.args[0]
    assert post.title == post.title
    assert post.content == post.content
    assert post.author == user_2posts
    assert resp.status_code == 200
    assert request.endpoint == 'main.home'


def test_new_post_get(client):
    resp = client.get('/post/new', follow_redirects=True)

    assert resp.status_code == 200
    assert request.endpoint == 'posts.new_post'


def test_post(req, client, loaded_db):
    resp = client.get('/post/1')

    assert resp.status_code == 200
    assert resp.content_length > 0
    assert b'test_title0' in resp.data
    assert request.endpoint == 'posts.post'


@mock.patch('flaskblog.posts.routes.Post', spec=True)
def test_update_post_get(mock_post, req, client, user_2posts, post):
    mock_post.query.get_or_404.return_value = post
    with mock.patch('flaskblog.posts.routes.current_user', user_2posts):
        resp = client.get('/post/1/update')

        assert b'test_title0' in resp.data
        assert b'test_content0' in resp.data
        assert resp.status_code == 200
        assert request.endpoint == 'posts.update_post'


@pytest.mark.parametrize('client, user_2posts, loaded_db', [(None, None, None)], indirect=True)
@pytest.mark.parametrize('post_id, expected_status', [(3, 403), (4, 404)])
def test_update_post_get_fail(client, user_2posts, loaded_db, post_id, expected_status):
    with mock.patch('flaskblog.posts.routes.current_user', user_2posts):
        resp = client.get(f'/post/{post_id}/update')

        assert resp.status_code == expected_status


@mock.patch('flaskblog.posts.routes.db')
def test_update_post_post(mock_db, req, client, user_2posts, loaded_db):
    with mock.patch('flaskblog.posts.routes.current_user', user_2posts):
        resp = client.post('/post/1/update', data={'title': 'New Title',
                                                   'content': 'New Content'}, follow_redirects=True)

        mock_db.session.commit.assert_called_once()
        assert resp.status_code == 200
        assert request.endpoint == 'posts.post'


@mock.patch('flaskblog.posts.routes.db')
def test_delete_post(mock_db, req, client, user_2posts, loaded_db):
    with mock.patch('flaskblog.posts.routes.current_user', user_2posts):
        resp = client.post('/post/1/delete', data={}, follow_redirects=True)

        mock_db.session.delete.assert_called_once()
        mock_db.session.commit.assert_called_once()
        assert resp.status_code == 200
        assert request.endpoint == 'main.home'
