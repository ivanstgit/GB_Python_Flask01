from flask import Blueprint, render_template
from blog.models import Author

author_app = Blueprint(
    "author_app", __name__, static_folder="../static"
)


@author_app.route("/", endpoint="list")
def list():
    authors = Author.query.all()
    return render_template("authors/list.html", authors=authors)
