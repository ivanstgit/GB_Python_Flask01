from flask import Blueprint, current_app, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from werkzeug.exceptions import NotFound

from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError

from blog.forms.article import CreateArticleForm
from blog.models.article import Article
from blog.models.author import Author
from blog.models.database import db
from blog.models.tag import Tag

article_app = Blueprint(
    "article_app", __name__, static_folder="../static"
)


@article_app.route("/", endpoint="list")
def get_list():
    articles = Article.query.all()
    return render_template("articles/list.html", articles=articles)


@article_app.route("/REST/", endpoint="list2")
def get_list_from_REST():
    return render_template("articles/list_REST.html")


@article_app.route("/<int:id>/", endpoint="details")
def get_details(id: int):
    article = (
        Article.query.filter_by(id=id)
        .options(joinedload(Article.tags))  # подгружаем связанные теги!
        .one_or_none()
    )
    if article is None:
        raise NotFound
    return render_template("articles/details.html", article=article)


@article_app.route("/create/", methods=["GET", "POST"], endpoint="create")
@login_required
def create_article():
    error = None
    form = CreateArticleForm(request.form)
    # добавляем доступные теги в форму
    form.tags.choices = [(tag.id, tag.name)
                         for tag in Tag.query.order_by("name")]

    if request.method == "POST" and form.validate_on_submit():
        if current_user.author:  # type: ignore
            # use existing author if present
            article_author = current_user.author  # type: ignore
        else:
            # otherwise create author record
            article_author = Author(user_id=current_user.id)  # type: ignore
            db.session.add(article_author)
            # db.session.flush()

        article = Article(title=form.title.data.strip(),
                          body=form.body.data)  # type: ignore
        article.author = article_author
        if form.tags.data:  # если в форму были переданы теги (были выбраны)
            selected_tags = Tag.query.filter(Tag.id.in_(form.tags.data))
            for tag in selected_tags:
                article.tags.append(tag)  # добавляем выбранные теги к статье

        db.session.add(article)

        try:
            db.session.commit()
        except IntegrityError:
            current_app.logger.exception("Could not create a new article!")  # type: ignore
            error = "Could not create article!"
        else:
            return redirect(url_for("article_app.details", id=article.id))
    return render_template("articles/create.html", form=form, error=error)
