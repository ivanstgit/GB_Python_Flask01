from flask import Blueprint, render_template
from werkzeug.exceptions import NotFound

user = Blueprint("user", __name__, url_prefix="/users", static_folder="../static")

USERS = {
    1: "James",
    2: "Brian",
    3: "Peter",
}


@user.route("/", endpoint="list")
def list():
    return render_template("/users/list.html", users=USERS)


@user.route("/<int:id>/", endpoint="details")
def details(id: int):
    try:
        name = USERS[id]
    except KeyError:
        raise NotFound(f"User #{id} doesn't exist!")
    return render_template("/users/details.html", id=id, name=name)
