import mock
from flask import request


@mock.patch('flaskblog.posts.routes.db')
def test_new_post_post(mock_db, req, client, post, user_2posts, session):
    """
    Test creating a new post when the NewPost form is submitted and the user is redirected properly.
    """

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
    """
    Test that the new post endpoint loads correctly.
    """

    resp = client.get('/post/new', follow_redirects=True)

    assert resp.status_code == 200
    assert request.endpoint == 'posts.new_post'


def test_post(req, client, post, loaded_db):
    """
    Test the endpoint for retrieving a specific post.
    """

    resp = client.get(f'/post/{post.id}')

    assert resp.status_code == 200
    assert resp.content_length > 0
    assert post.title in str(resp.data)
    assert request.endpoint == 'posts.post'


@mock.patch('flaskblog.posts.routes.Post', spec=True)
def test_update_post_get(mock_post, req, client, user_2posts, post, loaded_db):
    """
    Test the GET method for the update post endpoint.
    """

    mock_post.query.get_or_404.return_value = post
    with mock.patch('flaskblog.posts.routes.current_user', user_2posts):
        resp = client.get(f'/post/{post.id}/update')

        assert resp.status_code == 200
        assert request.endpoint == 'posts.update_post'
        assert b'test_title0' in resp.data
        assert b'test_content0' in resp.data


def test_update_post_get_fail_404(client, user_2posts, loaded_db):
    """
    Test that the GET method for the update post endpoint throws a 404 error when accessing a post that doesn't exist.
    """

    with mock.patch('flaskblog.posts.routes.current_user', user_2posts):
        resp = client.get('/post/-1/update')

        assert resp.status_code == 404


def test_update_post_get_fail_403(client, user_0post, user_2posts, loaded_db):
    """
    Test that the GET method for the update post endpoint throws a 404 error when accessing a post that belong to the
    current user.
    """

    with mock.patch('flaskblog.posts.routes.current_user', user_0post):
        resp = client.get(f'/post/{user_2posts.posts[0].id}/update')

        assert resp.status_code == 403


@mock.patch('flaskblog.posts.routes.db')
def test_update_post_post(mock_db, req, client, user_2posts, loaded_db):
    """
    Test the POST method to the update post endpoint causes the post to be properly updated.
    """

    with mock.patch('flaskblog.posts.routes.current_user', user_2posts):
        resp = client.post(f'/post/{user_2posts.posts[0].id}/update', data={'title': 'New Title',
                                                                            'content': 'New Content'}, follow_redirects=True)

        mock_db.session.commit.assert_called_once()
        assert resp.status_code == 200
        assert request.endpoint == 'posts.post'


@mock.patch('flaskblog.posts.routes.db')
def test_delete_post(mock_db, req, client, user_2posts, loaded_db):
    """
    Test that the delete post endpoint deletes the specified post.
    """

    with mock.patch('flaskblog.posts.routes.current_user', user_2posts):
        resp = client.post(f'/post/{user_2posts.posts[0].id}/delete', data={}, follow_redirects=True)

        mock_db.session.delete.assert_called_once()
        mock_db.session.commit.assert_called_once()
        assert resp.status_code == 200
        assert request.endpoint == 'main.home'
