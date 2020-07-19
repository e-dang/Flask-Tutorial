from flaskblog.posts.forms import PostForm
from flaskblog.models import Post
from flaskblog import db
from flask_login import current_user, login_required
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint

posts = Blueprint('posts', __name__)


@posts.route('/post/new', methods=['POST', 'GET'])
@login_required
def new_post():
    """
    The Create_Post page route that allows a user to create a new post to the blog. When a post has been successfully
    created, this page redirects to the Home page. Uses the PostForm.
    """

    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')


@posts.route('/post/<int:post_id>')
def post(post_id):
    """
    The Post page route that allows someone to view a single post. If that person is the author of the post they will
    have the option to update or delete the post. In either case this page will redirect to the update_post or
    delete_post routes.
    """

    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route('/post/<int:post_id>/update', methods=['POST', 'GET'])
@login_required
def update_post(post_id):
    """
    The route used to update a post. It displays the create_post.html page with the original posts contents filled in,
    and allows the user to change anything about the post. When the post has been successfully updated it redirects to
    the post route.
    """

    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')


@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    """
    The route used to delete post. If the user is not the author of the post then it aborts with a 403 error. Otherwise
    the post is deleted and the user is redirected to the home route.
    """

    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))
