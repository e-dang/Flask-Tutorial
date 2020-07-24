import pytest
from flask import request


@pytest.mark.parametrize('client, loaded_db, url', [
    (None, None, '/'),
    (None, None, '/home'),
],
    indirect=['client', 'loaded_db'])
def test_home(client, loaded_db, url):
    """
    Test that both aliases for the home page lead to the correct endpoint and that posts are ordered from earliest to
    latest.
    """

    resp = client.get(url)

    assert resp.status_code == 200
    assert resp.content_length > 0
    assert request.endpoint == 'main.home'
    assert b'<title>Flask Blog</title>' in resp.data
    str_data = str(resp.data)
    assert str_data.find('test_title0') > str_data.find('test_title1') > str_data.find('test_title2')


def test_about(client):
    """
    Test that the about page url leads to the correct endpoint.
    """

    resp = client.get('/about')

    assert resp.status_code == 200
    assert resp.content_length > 0
    assert request.endpoint == 'main.about'
    assert b'<title>Flask Blog - About</title>' in resp.data
