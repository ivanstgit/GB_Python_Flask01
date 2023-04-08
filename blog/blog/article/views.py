from datetime import date
from flask import Blueprint, render_template
from werkzeug.exceptions import NotFound

from blog.user.views import USERS

article = Blueprint(
    "article", __name__, url_prefix="/articles", static_folder="../static"
)

ARTICLES = {
    1: {
        "author": 3,
        "title": "Article 1",
        "content": "Article content 1",
        "posted": date(2021, 12, 1),
    },
    2: {
        "author": 2,
        "title": "Article 2",
        "content": "Article content 2",
        "posted": date(2021, 11, 12),
    },
    3: {
        "author": 1,
        "title": "Article 3",
        "content": "Article content 3",
        "posted": date(2021, 11, 11),
    },
}


@article.route("/", endpoint="list")
def list():
    return render_template("/articles/list.html", articles=ARTICLES, users=USERS)


@article.route("/<int:id>/", endpoint="details")
def details(id: int):
    try:
        article = ARTICLES[id]
        author = article.get("author")
        if author:
            user = USERS.get(author)
        else:
            user = None
    except KeyError:
        raise NotFound(f"article #{id} doesn't exist!")
    return render_template(
        "/articles/details.html", id=id, article=article, author=user
    )
