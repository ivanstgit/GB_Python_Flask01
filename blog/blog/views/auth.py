from flask import (
    Blueprint,
    current_app,
    render_template,
    request,
    redirect,
    url_for,
)
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from sqlalchemy.exc import IntegrityError

from werkzeug.exceptions import NotFound
from blog.forms.user import LoginForm, RegistrationForm
from blog.models import User
from blog.models.database import db

auth_app = Blueprint("auth_app", __name__)
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).one_or_none()


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("auth.login"))


@auth_app.route("/login/", methods=["GET", "POST"], endpoint="login")
def login():
    if current_user.is_authenticated:  # type: ignore
        return redirect("index")

    form = LoginForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).one_or_none()
        if user is None:
            return render_template(
                "auth/login.html", form=form, error="invalid username or password"
            )
        if not user.validate_password(form.password.data):
            return render_template(
                "auth/login.html", form=form, error="invalid username or password"
            )
        login_user(user)
        return redirect(url_for("index"))
    return render_template("auth/login.html", form=form)


@auth_app.route("/login-as/", methods=["GET", "POST"], endpoint="login-as")  # type: ignore
def login_as():
    if not (current_user.is_authenticated and current_user.is_staff):  # type: ignore
        # non-admin users should not know about this feature
        raise NotFound


@auth_app.route("/logout/", endpoint="logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@auth_app.route("/register/", methods=["GET", "POST"], endpoint="register")
def register():
    if current_user.is_authenticated:  # type: ignore
        return redirect("index")

    error = None
    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).count():
            form.email.errors.append("user with this e-mail already exists!")  # type: ignore
            return render_template("auth/register.html", form=form)
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            is_staff=False,
        )
        user.password = form.password.data
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            current_app.logger.exception("Could not create user!")
            error = "Could not create user!"
        else:
            current_app.logger.info("Created user %s", user)
            login_user(user)
            return redirect(url_for("index"))
    return render_template("auth/register.html", form=form, error=error)


__all__ = [
    "login_manager",
    "auth_app",
]
