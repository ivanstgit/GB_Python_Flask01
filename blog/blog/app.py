import os
from flask import Flask, render_template
from flask_migrate import Migrate

from blog.models.database import db
from blog.models.user import User
from blog.security import flask_bcrypt
from blog.views.auth import auth, login_manager
from blog.views.user import views as users
from blog.views.author import views as authors
from blog.views.article import views as articles


def create_app() -> Flask:
    app = Flask(__name__)

    load_config(app)
    init_components(app)
    register_blueprints(app)

    @app.route("/")
    def index():
        return render_template("index.html")

    return app


def load_config(app: Flask):
    cfg_name = os.environ.get("CONFIG_NAME") or "BaseConfig"  # "ProductionConfig"
    app.config.from_object(f"blog.configs.{cfg_name}")


def init_components(app: Flask):
    # database
    db.init_app(app)
    migrate = Migrate(app, db, compare_type=True)

    # security
    flask_bcrypt.init_app(app)

    # login manager
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"  # type: ignore

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


def register_blueprints(app: Flask):
    app.register_blueprint(users.user)
    app.register_blueprint(authors.author)
    app.register_blueprint(articles.article)
    app.register_blueprint(auth)
