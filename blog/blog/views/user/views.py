from flask import Blueprint, render_template
from flask_login import login_required
from werkzeug.exceptions import NotFound

from blog.models.user import User

user_app = Blueprint(
    "user_app", __name__, static_folder="../static"
)


@user_app.route("/", endpoint="list")
def list():
    users = User.query.all()
    return render_template("/users/list.html", users=users)


@user_app.route("/<int:id>/", endpoint="details")
@login_required
def details(id: int):
    user = User.query.filter_by(id=id).one_or_none()
    if not user:
        raise NotFound(f"User #{id} doesn't exist!")
    return render_template("/users/details.html", user=user)


def get_user_desc(id: int):
    user = User.query.filter_by(id=id).one_or_none()
    if user:
        return str(user)
    return None
