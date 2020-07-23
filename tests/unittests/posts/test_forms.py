from flaskblog.posts import forms


def test_post_form(req, post):
    form = forms.PostForm(obj=post)

    form.submit()

    assert form.validate()
