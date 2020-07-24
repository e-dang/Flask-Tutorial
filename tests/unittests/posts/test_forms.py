from flaskblog.posts import forms


def test_post_form(req, post):
    """
    Test that verifies that the Post form validates the correct fields.
    """

    form = forms.PostForm(obj=post)

    form.submit()

    assert form.validate()
