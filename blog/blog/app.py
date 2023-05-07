import os
from flask import Flask, render_template
from flask_migrate import Migrate

from blog.api import init_api, register_api_routes
from blog.cli import register_commands
from blog.models.database import db

from blog.security import flask_bcrypt


def create_app() -> Flask:
    app = Flask(__name__)

    load_config(app)
    init_components(app)
    register_blueprints(app)
    register_commands(app)
    register_api_routes(url_prefix="/api")

    @app.route("/")
    def index():
        return render_template("index.html")

    return app


def load_config(app: Flask):
    cfg_name = os.environ.get("CONFIG_NAME") or "BaseConfig"  # "ProductionConfig"
    app.config.from_object(f"blog.configs.{cfg_name}")


def init_components(app: Flask):
    from blog.admin import admin

    # database
    db.init_app(app)
    migrate = Migrate(app, db, compare_type=True)

    # security
    flask_bcrypt.init_app(app)

    # admin
    admin.init_app(app)

    # login manager
    from blog.views.auth import login_manager
    from blog.models.user import User
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"  # type: ignore

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    init_api(app)


def register_blueprints(app: Flask):
    from blog.views.auth import auth_app
    from blog.views.user import views as users
    from blog.views.author import views as authors
    from blog.views.article import views as articles

    app.register_blueprint(users.user_app, url_prefix="/users")
    app.register_blueprint(authors.author_app, url_prefix="/authors")
    app.register_blueprint(articles.article_app, url_prefix="/articles")
    app.register_blueprint(auth_app)
