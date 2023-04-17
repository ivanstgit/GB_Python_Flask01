from flask import Blueprint, current_app, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from werkzeug.exceptions import NotFound

from sqlalchemy.exc import IntegrityError

from blog.forms.article import CreateArticleForm
from blog.models.article import Article
from blog.models.author import Author
from blog.models.database import db

article = Blueprint(
    "article", __name__, url_prefix="/articles", static_folder="../static"
)


@article.route("/", endpoint="list")
def get_list():
    articles = Article.query.all()
    return render_template("articles/list.html", articles=articles)


@article.route("/<int:id>/", endpoint="details")
def get_details(id: int):
    article = Article.query.filter_by(id=id).one_or_none()
    if article is None:
        raise NotFound
    return render_template("articles/details.html", article=article)


@article.route("/create/", methods=["GET", "POST"], endpoint="create")
@login_required
def create_article():
    error = None
    form = CreateArticleForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        if current_user.author:  # type: ignore
            # use existing author if present
            article_author = current_user.author  # type: ignore
        else:
            # otherwise create author record
            article_author = Author(user_id=current_user.id)  # type: ignore
            db.session.add(article_author)
            # db.session.flush()

        article = Article(title=form.title.data.strip(), body=form.body.data)
        article.author = article_author
        db.session.add(article)
        try:
            db.session.commit()
        except IntegrityError:
            current_app.logger.exception("Could not create a new article!")
            error = "Could not create article!"
        else:
            return redirect(url_for("article.details", id=article.id))
    return render_template("articles/create.html", form=form, error=error)
