from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_login import LoginManager
from flask_bootstrap import Bootstrap


db = SQLAlchemy()
login = LoginManager()


def create_application():
    app = Flask(
        __name__,
        static_url_path='/static',
        static_folder='static',
        template_folder='templates'
    )

    app.config.from_object(Config)

    db.init_app(app)

    Migrate(app, db)

    login.init_app(app)
    login.login_view = 'index.login'
    bootstrap = Bootstrap(app)

    from app.index import bp as index_blueprint
    app.register_blueprint(index_blueprint)

    from app.errors import bp as errors_blueprint
    app.register_blueprint(errors_blueprint)

    return app


# from app import routes, models, errors
