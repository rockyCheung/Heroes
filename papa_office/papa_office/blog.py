import datetime
import functools
import uuid

from bson.objectid import ObjectId
from flask import (
    Flask, flash, render_template, session, request, redirect, url_for)
from pymodm.errors import ValidationError
from pymongo.errors import DuplicateKeyError

from papa_office.models.blog_models import User, Post, Comment
from papa_office.models.MongoModels import Keys,Post

# Secret key used to encrypt session cookies.
# We'll just generate one randomly when the app starts up, since this is just
# a demonstration project.
SECRET_KEY = str(uuid.uuid4())


app = Flask(__name__)
app.secret_key = SECRET_KEY


def human_date(value, format="%B %d at %I:%M %p"):
    """Format a datetime object to be human-readable in a template."""
    return value.strftime(format)
app.jinja_env.filters['human_date'] = human_date


def logged_in(func):
    """Decorator that redirects to login page if a user is not logged in."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return wrapper


@app.route('/posts/new', methods=['GET', 'POST'])
@logged_in
def create_post():
    if request.method == 'GET':
        return render_template('new_post.html')
    else:
        if request.form['date']:
            post_date = request.form['date']
        else:
            post_date = datetime.datetime.now()
        try:
            Post(title=request.form['title'],
                 date=post_date,
                 body=request.form['content'],
                 author=session['user']).save()
        except ValidationError as exc:
            return render_template('new_post.html', errors=exc.message)
        return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # Return login form.
        return render_template('login.html')
    else:
        # Login.
        email, password = request.form['email'], request.form['password']
        try:
            # Note: logging users in like this is acceptable for demonstration
            # projects only.
            user = User.objects.get({'_id': email, 'password': password})
        except User.DoesNotExist:
            return render_template('login.html', error='Bad email or password')
        else:
            # Store user in the session.
            session['user'] = user.email
            return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been successfully logged out.')
    return redirect(url_for('index'))


@app.route('/users/new', methods=['GET', 'POST'])
def new_user():
    if request.method == 'GET':
        return render_template('new_user.html')
    else:
        try:
            # Note: real applications should handle user registration more
            # securely than this.
            User(email=request.form['email'],
                 handle=request.form['handle'],
                 # Use `force_insert` so that we get a DuplicateKeyError if
                 # another user already exists with the same email address.
                 # Without this option, we will update (replace) the user with
                 # the same id (email).
                 password=request.form['password']).save(force_insert=True)
        except ValidationError as ve:
            return render_template('new_user.html', errors=ve.message)
        except DuplicateKeyError:
            # Email address must be unique.
            return render_template('new_user.html', errors={
                'email': 'There is already a user with that email address.'
            })
    return redirect(url_for('index'))


@app.route('/')
def index():
    # Use a list here so we can do "if posts" efficiently in the template.
    return render_template('index.html', posts=list(Post.objects.all()))


@app.route('/posts/<post_id>')
def get_post(post_id):
    try:
        # `post_id` is a string, but it's stored as an ObjectId in the database.
        post = Post.objects.get({'_id': ObjectId(post_id)})
    except Post.DoesNotExist:
        return render_template('404.html'), 404
    return render_template('post.html', post=post)


@app.route('/comments/new', methods=['POST'])
def new_comment():
    post_id = ObjectId(request.form['post_id'])
    try:
        post = Post.objects.get({'_id': post_id})
    except Post.DoesNotExist:
        flash('No post with id: %s' % post_id)
        return redirect(url_for('index'))
    comment = Comment(
        author=request.form['author'],
        date=datetime.datetime.now(),
        body=request.form['content'])
    post.comments.append(comment)
    try:
        post.save()
    except ValidationError as e:
        post.comments.pop()
        comment_errors = e.message['comments'][-1]
        return render_template('post.html', post=post, errors=comment_errors)
    flash('Comment saved successfully.')
    return render_template('post.html', post=post)

# User(email='test@qq.com',
#          handle='handle',
#          # Use `force_insert` so that we get a DuplicateKeyError if
#          # another user already exists with the same email address.
#          # Without this option, we will update (replace) the user with
#          # the same id (email).
#          password='pass').save(force_insert=True)
# user = Keys.objects.get({'_id': '5a4c6f26421aa90815800a1b'})
# print user.status
# keys = Keys.objects.get({'status': 1,'sflag':0})
# print keys.key
# user = User.objects.get({'_id':'mongoblogger@reallycoolmongostuff.com'})
# print user.email
# def main():
#     app.run(debug=True)
#
#
# if __name__ == '__main__':
#     main()