import mock
import os
from flaskblog.users import utils


@mock.patch('flaskblog.users.utils.secrets')
@mock.patch('flaskblog.users.utils.Image')
def test_save_picture(mock_image, mock_secrets, app):
    """
    Test that the save_picture utility function manipulates the picture name properly.
    """

    random_hex = 'random_hex'
    ext = '.png'
    mock_secrets.token_hex.return_value = random_hex
    mock_image.open.return_value = mock_image
    mock_form_picture = mock.MagicMock()
    mock_form_picture.configure_mock(filename='test_filename' + ext)

    picture_filename = utils.save_picture(mock_form_picture)

    mock_image.thumbnail.assert_called_once()
    mock_image.save.assert_called_once()
    mock_image.save.assert_called_with(os.path.join(app.root_path, 'static', 'profile_pics', picture_filename))
    assert picture_filename == random_hex + '.png'


@mock.patch('flaskblog.users.utils.Message')
@mock.patch('flaskblog.users.utils.mail')
def test_send_reset_email(mock_mail, mock_message, req):
    """
    Test that the send_reset_email sends an email with the reset_token inside of it.
    """

    reset_token = 'random_reset_token'
    mock_user = mock.MagicMock()
    mock_user.get_reset_token.return_value = reset_token
    mock_message.return_value = mock_message

    utils.send_reset_email(mock_user)

    assert reset_token in mock_message.body
    mock_mail.send.assert_called_once()
