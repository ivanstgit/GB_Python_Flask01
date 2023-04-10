from json import load
from os import getenv, path
from flask import Flask, render_template

from blog.models.database import db
from blog.models.user import User
from blog.views.auth import auth, login_manager
from blog.views.user import views as users
from blog.views.article import views as articles

CONFIG_PATH = getenv("CONFIG_PATH", path.join("..", "config_dev.json"))


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_file(CONFIG_PATH, load)

    init_components(app)
    register_blueprints(app)

    @app.route("/")
    def index():
        return render_template("index.html")

    return app


def init_components(app: Flask):
    # database
    db.init_app(app)

    # login manager
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"  # type: ignore

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


def register_blueprints(app: Flask):
    app.register_blueprint(users.user)
    app.register_blueprint(articles.article)
    app.register_blueprint(auth)
