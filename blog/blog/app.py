from flask import Flask, render_template

from blog.user import views as users
from blog.article import views as articles


def create_app() -> Flask:
    app = Flask(__name__)
    register_blueprints(app)

    @app.route("/")
    def index():
        return render_template("index.html")

    return app


def register_blueprints(app: Flask):
    app.register_blueprint(users.user)
    app.register_blueprint(articles.article)
