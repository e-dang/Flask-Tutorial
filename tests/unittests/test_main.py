import pytest
from flask import request


@pytest.mark.parametrize('client', [None], indirect=['client'])
@pytest.mark.parametrize('url', ['/', '/home'])
def test_home(client, url):
    resp = client.get(url)

    assert resp.status_code == 200
    assert resp.content_length > 0
    assert request.endpoint == 'main.home'
    assert b'<title>Flask Blog</title>' in resp.data


def test_about(client):
    resp = client.get('/about')

    assert resp.status_code == 200
    assert resp.content_length > 0
    assert request.endpoint == 'main.about'
    assert b'<title>Flask Blog - About</title>' in resp.data
