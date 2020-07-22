from flask_wtf.csrf import generate_csrf

from flaskblog.posts import forms


def test_post_form(req, post):
    form = forms.PostForm(obj=post, csrf_token=generate_csrf())

    form.submit()

    assert form.validate()
