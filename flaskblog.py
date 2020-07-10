from flask import Flask, render_template, url_for
from forms import RegistrationForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '9ab13cd77620a65a973c7e09d00653b4'

posts = [
    {
        'author': 'Eric Dang',
        'title': 'Blog Post 1',
        'content': 'This is the first post',
        'date_posted': 'July 9, 2020'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'This is the second post',
        'date_posted': 'July 10, 2020'
    }
]


@app.route('/')
@app.route('/home')
def hello():
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register')
def register():
    form = RegistrationForm()
    return render_template('register.html', title='Register', form=form)


if __name__ == "__main__":
    app.run(debug=True)
