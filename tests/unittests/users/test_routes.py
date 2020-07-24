import pytest
import mock
from flask import request
from flaskblog.models import load_user


@pytest.mark.parametrize('client, authenticated', [
    (None, True),
    (None, False)
],
    indirect=['client'],
    ids=['is_authenticated', 'is_not_authenticated'])
def test_register_get(client, authenticated, session):
    with mock.patch('flaskblog.users.routes.current_user') as mock_current_user:
        mock_current_user.configure_mock(is_authenticated=authenticated)
        resp = client.get('/register', follow_redirects=True)

        assert resp.status_code == 200
        if authenticated:
            assert request.endpoint == 'main.home'
        else:
            assert request.endpoint == 'users.register'


@mock.patch('flaskblog.users.routes.current_user')
@mock.patch('flaskblog.users.routes.db')
def test_register_post(mock_db, mock_current_user, client, user_0post, session):
    mock_current_user.configure_mock(is_authenticated=False)
    resp = client.post('/register', data={'username': user_0post.username,
                                          'email': user_0post.email,
                                          'password': user_0post.password,
                                          'confirm_password': user_0post.password}, follow_redirects=True)

    mock_db.session.add.assert_called_once()
    mock_db.session.commit.assert_called_once()
    assert resp.status_code == 200
    assert request.endpoint == 'users.login'


@pytest.mark.parametrize('client, authenticated', [
    (None, True),
    (None, False)
],
    indirect=['client'],
    ids=['is_authenticated', 'is_not_authenticated'])
def test_login_get(client, authenticated, session):
    with mock.patch('flaskblog.users.routes.current_user') as mock_current_user:
        mock_current_user.configure_mock(is_authenticated=authenticated)
        resp = client.get('/login', follow_redirects=True)

        assert resp.status_code == 200
        if authenticated:
            assert request.endpoint == 'main.home'
        else:
            assert request.endpoint == 'users.login'


@pytest.mark.parametrize('client, loaded_db, user_2posts, next_page, endpoint', [
    (None, True, None, None, 'main.home'),
    (None, True, None, 'account', 'users.account')
],
    indirect=['client', 'loaded_db', 'user_2posts'],
    ids=['no_specific_next_page', 'specific_next_page'])
def test_login_post(client, loaded_db, user_2posts, next_page, endpoint):
    with mock.patch('flaskblog.users.routes.current_user') as mock_current_user, \
            mock.patch('flaskblog.users.routes.login_user') as mock_login_user:
        mock_current_user.configure_mock(is_authenticated=False)
        resp = client.post('/login', data={'email': user_2posts.email,
                                           'password': f'test_password0'}, query_string={'next': next_page},
                           follow_redirects=True)

        mock_login_user.assert_called_once()
        mock_login_user.assert_called_with(user_2posts, remember=False)
        assert resp.status_code == 200
        assert request.endpoint == endpoint


@pytest.mark.parametrize('client, loaded_db', [
    (None, True)
],
    indirect=['client', 'loaded_db'])
def test_login_post_fail(client, loaded_db):
    with mock.patch('flaskblog.users.routes.current_user') as mock_current_user, \
            mock.patch('flaskblog.users.routes.login_user') as mock_login_user, \
            mock.patch('flaskblog.users.routes.flash') as mock_flash:
        mock_current_user.configure_mock(is_authenticated=False)
        resp = client.post('/login', data={'email': 'test_email0@demo.com',
                                           'password': 'Wrong password'})

        mock_login_user.assert_not_called()
        mock_flash.assert_called_once()
        assert resp.status_code == 200
        assert 'Login Unsuccessful'.lower() in mock_flash.call_args.args[0].lower()


@mock.patch('flaskblog.users.routes.logout_user')
def test_logout(mock_log_out, client, session):
    resp = client.get('/logout', follow_redirects=True)

    mock_log_out.assert_called_once()
    assert resp.status_code == 200
    assert request.endpoint == 'main.home'


@mock.patch('flaskblog.users.routes.url_for')
@mock.patch('flaskblog.users.routes.current_user')
@mock.patch('flaskblog.users.routes.UpdateAccountForm')
def test_account_get(mock_account_form, mock_current_user, mock_url_for, client):
    mock_account_form.return_value = mock_account_form
    mock_account_form.validate_on_submit.return_value = False
    mock_current_user.configure_mock(username='TestUser', email='test_user@demo.com', image_file='test_image.png')

    resp = client.get('/account', follow_redirects=True)

    assert mock_account_form.username.data == mock_current_user.username
    assert mock_account_form.email.data == mock_current_user.email
    assert resp.status_code == 200
    assert request.endpoint == 'users.account'


@pytest.mark.parametrize('client, session, data', [
    (None, None, {'username': 'TestUser',
                  'email': 'test_user@demo.com',
                  'picture': 'test_image.png'}),
    (None, None, {'username': 'TestUser',
                  'email': 'test_user@demo.com'})
],
    indirect=['client', 'session'],
    ids=['w_pic_data', 'no_pic_data'])
def test_account_post(client, session, data):
    hashed_image_file = 'hashed_image_file.png'
    default_image_file = 'default_image.png'
    with mock.patch('flaskblog.users.routes.save_picture') as mock_save_picture, \
            mock.patch('flaskblog.users.routes.db') as mock_db, \
            mock.patch('flaskblog.users.routes.current_user') as mock_current_user_routes, \
            mock.patch('flaskblog.users.forms.current_user') as mock_current_user_forms:
        mock_current_user_routes.image_file = default_image_file
        mock_current_user_forms.username = 'random user name'
        mock_save_picture.return_value = hashed_image_file
        resp = client.post('/account', data=data, follow_redirects=True)

        mock_db.session.commit.assert_called_once()
        assert mock_current_user_routes.username == data['username']
        assert mock_current_user_routes.email == data['email']
        assert mock_current_user_routes.image_file == default_image_file if data.get(
            'picture') is None else hashed_image_file
        assert resp.status_code == 200
        assert request.endpoint == 'users.account'


def test_user_posts(client, user_2posts, loaded_db):
    resp = client.get(f'/user/{user_2posts.username}', query_string={'page': 1})

    assert resp.status_code == 200
    assert request.endpoint == 'users.user_posts'
    response_data = str(resp.data)
    assert response_data.find('test_title0') > response_data.find('test_title1')


def test_user_posts_fail(client, user_2posts, loaded_db):
    resp = client.get(f'/user/{user_2posts.username}', query_string={'page': 1000})

    assert resp.status_code == 404


@pytest.mark.parametrize('client, session, authenticated, endpoint', [
    (None, None, True, 'main.home'),
    (None, None, False, 'users.reset_request')
],
    indirect=['client', 'session'],
    ids=['is_authenticated', 'not_authenticated'])
def test_reset_request_get(client, session, authenticated, endpoint):
    with mock.patch('flaskblog.users.routes.current_user') as mock_current_user:
        mock_current_user.configure_mock(is_authenticated=authenticated)
        resp = client.get('/reset_password', follow_redirects=True)

        assert resp.status_code == 200
        assert request.endpoint == endpoint


def test_reset_request_post(client, user_1post, loaded_db):
    with mock.patch('flaskblog.users.routes.current_user') as mock_current_user, \
            mock.patch('flaskblog.users.routes.send_reset_email') as mock_send_reset_email:
        mock_current_user.configure_mock(is_authenticated=False)
        resp = client.post('/reset_password', data={'email': user_1post.email}, follow_redirects=True)

        mock_send_reset_email.assert_called_once()
        mock_send_reset_email.assert_called_with(user_1post)
        assert resp.status_code == 200
        assert request.endpoint == 'users.login'


@pytest.mark.parametrize('client, session, user_1post, authenticated, verified, endpoint', [
    (None, None, None, True, False, 'main.home'),
    (None, None, None, False, True, 'users.reset_token'),
    (None, None, None, False, False, 'users.reset_request')
],
    indirect=['client', 'session', 'user_1post'],
    ids=['is_authenticated', 'not_authenticated_and_verified', 'not_authenticated_and_not_verified'])
def test_reset_token_get(client, session, user_1post, authenticated, verified, endpoint):
    with mock.patch('flaskblog.users.routes.current_user') as mock_current_user, \
            mock.patch('flaskblog.users.routes.User') as mock_user_class:
        mock_user_class.verify_reset_token.return_value = user_1post if verified else None
        mock_current_user.configure_mock(is_authenticated=authenticated)
        resp = client.get('/reset_password/random_token', follow_redirects=True)

        assert resp.status_code == 200
        assert request.endpoint == endpoint


def test_reset_token_post(client, user_1post):
    new_password = 'New Password'
    hashed_new_password = b'Hashed new password'
    with mock.patch('flaskblog.users.routes.db') as mock_db, \
            mock.patch('flaskblog.users.routes.current_user') as mock_current_user, \
            mock.patch('flaskblog.users.routes.User') as mock_user_class, \
            mock.patch('flaskblog.users.routes.bcrypt.generate_password_hash') as mock_generate_password_hash:
        mock_generate_password_hash.return_value = hashed_new_password
        mock_user_class.verify_reset_token.return_value = user_1post
        mock_current_user.configure_mock(is_authenticated=False)
        resp = client.post('/reset_password/random_token', data={'password': new_password,
                                                                 'confirm_password': new_password}, follow_redirects=True)

        mock_db.session.commit.assert_called_once()
        assert user_1post.password == hashed_new_password.decode('utf-8')
        assert resp.status_code == 200
        assert request.endpoint == 'users.login'
