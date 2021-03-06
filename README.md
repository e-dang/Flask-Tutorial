# Flask-Tutorial ![Travis (.com) branch](https://img.shields.io/travis/com/e-dang/Flask-Tutorial/master?label=master) ![Travis (.com) branch](https://img.shields.io/travis/com/e-dang/Flask-Tutorial/dev?label=dev)

## Description
The purpose of this project is to help me gain experience working with Flask, associated Flask plugins, unit testing, Docker, Travis CI, Git, and Heroku by following the [Flask tutorial made by Corey M. Schafer](https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/Flask_Blog). Example posts were taken from his tutorial. While much of the blog website was designed by Corey M. Schafer, his tutorial did not cover unit testing and the use of Docker, Travis CI, Git, and Heroku. All development on this project was tracked using the Gitflow workflow and done inside a Debian 10 (Python 3.8.3) Docker container with a mounted volume on my local filesystem. During development SQLite was initially used as the database, but I eventually switched to a PostgreSQL database through Dockercompose and the postgres Docker image. There are two corresponding unit testing configurations, one for testing locally that uses an in-memory SQLite database, and one for continuous integration tests on Travis CI that uses a PostgreSQL Docker container. Travis CI was also setup to perform continuous deployment to my Dockerhub and to Heroku through their Docker registry.

## Frameworks & Technologies
- Flask
- Flask-WTForms
- Flask-SQLAlchemy
- Flask-Bcrypt
- Flask-Login
- Flask-Mail
- pytest
- Gunicorn
- Docker
- Travis CI
- Heroku
- PostgreSQL
- SQLite

### Checkout the [FlaskBlog](https://edang-flaskblog.herokuapp.com/)!