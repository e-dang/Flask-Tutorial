import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import configs
from random import randint

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=os.environ.get('MY_FLASK_APP_CONFIG', 'dev'), **kwargs):
    app = Flask(__name__)
    app.config.from_object(configs[config_class])
    app.config.from_mapping(kwargs)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from flaskblog.users.routes import users  # noqa
    from flaskblog.posts.routes import posts  # noqa
    from flaskblog.main.routes import main  # noqa
    from flaskblog.errors.handlers import errors  # noqa

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    random_links = ['https://github.com/e-dang',
                    'https://github.com/e-dang/Composite-Peptide-Macrocycle-Generator',
                    'https://github.com/e-dang/ConfBusterPlusPlus',
                    'https://github.com/e-dang/dotfiles',
                    'https://github.com/e-dang/K-Means',
                    'https://github.com/e-dang/K-Medoids',
                    'https://www.nba.com/warriors/',
                    'https://www.ucla.edu/',
                    'https://www.jbc.org/content/293/49/19038.short']
    app.jinja_env.globals['rand_link'] = lambda: random_links[randint(0, len(random_links) - 1)]

    with app.app_context():
        db.create_all()

    return app
