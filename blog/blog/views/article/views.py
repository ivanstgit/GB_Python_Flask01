from datetime import date
from flask import Blueprint, render_template
from werkzeug.exceptions import NotFound
from blog.views.user.views import get_user_desc

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
def get_list():
    articles = [
        {
            "id": k,
            "author": v.get("author"),
            "author_name": get_user_desc(v.get("author", 0)),
            "title": v.get("title", ""),
            "posted": v.get("posted", ""),
        }
        for k, v in ARTICLES.items()
    ]

    return render_template("/articles/list.html", articles=articles)


@article.route("/<int:id>/", endpoint="details")
def get_details(id: int):
    try:
        article = ARTICLES[id]
        author = article.get("author")
        if author:
            user = get_user_desc(author)
        else:
            user = None
    except KeyError:
        raise NotFound(f"article #{id} doesn't exist!")
    return render_template(
        "/articles/details.html", id=id, article=article, author=user
    )
