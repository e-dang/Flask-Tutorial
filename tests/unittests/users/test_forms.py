import pytest
import mock
from flaskblog.users import forms


def test_registration_form(req, user_0post, session):
    form = forms.RegistrationForm(obj=user_0post, confirm_password=user_0post.password)

    form.submit()

    assert form.validate()


@pytest.mark.parametrize('req, loaded_db, username, email, password, confirm_password, error_attr, expect_num_errors', [
    (None, None, 'test_user0', 'test_email@demo.com', 'test_password', 'test_password', 'username', 1),
    (None, None, None, 'test_email@demo.com', 'test_password', 'test_password', 'username', 1),
    (None, None, 't', 'test_email@demo.com', 'test_password', 'test_password', 'username', 1),
    (None, None, 'toolongname123456789x', 'test_email@demo.com', 'test_password', 'test_password', 'username', 1),
    (None, None, 'test_user', 'test_email0@demo.com', 'test_password', 'test_password', 'email', 1),
    (None, None, 'test_user', 'test_email0', 'test_password', 'test_password', 'email', 1),
    (None, None, 'test_user', None, 'test_password', 'test_password', 'email', 1),
    (None, None, 'test_user', 'test_email@demo.com', 'test_password1', 'test_password', 'confirm_password', 1),
    (None, None, 'test_user', 'test_email@demo.com', None, 'test_password', 'password', 2),
    (None, None, 'test_user', 'test_email@demo.com', 'test_password', None, 'confirm_password', 1)
],
    indirect=['req', 'loaded_db'],
    ids=['taken_username', 'missing_username', 'username_too_short', 'username_too_long', 'taken_email', 'missing_email', 'invalid_email', 'mismatch_passwords', 'missing_password', 'missing_confirm_password'])
def test_registration_form_fail(req, loaded_db, username, email, password, confirm_password, error_attr, expect_num_errors):
    form = forms.RegistrationForm(username=username, email=email, password=password, confirm_password=confirm_password)

    form.submit()

    assert not form.validate()
    assert len(form.errors) == expect_num_errors
    assert error_attr in form.errors


def test_login_form(req, user_0post):
    form = forms.LoginForm(obj=user_0post)

    form.submit()

    assert form.validate()


def test_update_account_form(req, user_0post, loaded_db):
    with mock.patch('flaskblog.users.forms.current_user', user_0post):
        form = forms.UpdateAccountForm(username='New Username', email='new_email@demo.com', picture='pic.png')

        form.submit()

        assert form.validate()


@pytest.mark.parametrize('req, user_0post, loaded_db, username, email, picture, error_attr, expected_num_errors', [
    (None, None, None, 'test_user0', 'new_email@demo.com', 'pic.png', 'username', 1),
    (None, None, None, 'new_user', 'test_email0@demo.com', 'pic.png', 'email', 1)
],
    indirect=['req', 'user_0post', 'loaded_db'],
    ids=['taken_username', 'taken_email'])
def test_update_account_form_fail(req, user_0post, loaded_db, username, email, picture, error_attr, expected_num_errors):
    with mock.patch('flaskblog.users.forms.current_user', user_0post):
        form = forms.UpdateAccountForm(username=username, email=email, picture=picture)

        form.submit()

        assert not form.validate()
        assert len(form.errors) == expected_num_errors
        assert error_attr in form.errors


def test_request_reset_form(req, user_0post, loaded_db):
    form = forms.RequestResetForm(email=user_0post.email)

    form.submit()

    assert form.validate()


def test_request_reset_form_fail(req, loaded_db):
    form = forms.RequestResetForm(email='no_email@demo.com')

    form.submit()

    assert not form.validate()


def test_reset_password_form(req):
    form = forms.ResetPasswordForm(password='New Password', confirm_password='New Password')

    form.submit()

    assert form.validate()


@pytest.mark.parametrize('req, password, confirm_password, expected_num_errors, error_attr', [
    (None, 'test_password', 'test_password1', 1, 'confirm_password'),
    (None, None, 'test_password', 2, 'password'),
    (None, 'test_password', None, 1, 'confirm_password')
],
    indirect=['req'],
    ids=['mismatch_passwords', 'missing_password', 'missing_confirm_password'])
def test_reset_password_form_fail(req, password, confirm_password, expected_num_errors, error_attr):
    form = forms.ResetPasswordForm(password=password, confirm_password=confirm_password)

    form.submit()

    assert not form.validate()
    assert len(form.errors) == expected_num_errors
    assert error_attr in form.errors
