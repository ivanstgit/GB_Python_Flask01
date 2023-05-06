from flask import redirect, url_for
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose
from flask_admin.form import SecureForm
from flask_login import current_user

# from blog import models
from blog.models.article import Article

# from blog.models.tag import Tag
# from blog.models.user import User


class CustomAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        if not (current_user.is_authenticated and current_user.is_staff):  # type: ignore
            return redirect(url_for("auth_app.login"))
        return super(CustomAdminIndexView, self).index()


# Customized admin interface
class CustomAdminView(ModelView):
    form_base_class = SecureForm

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_staff  # type: ignore

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for("auth_app.login"))


class TagAdminView(CustomAdminView):
    column_searchable_list = ("name",)
    column_filters = ("name",)
    can_export = True
    export_types = ["csv", "xlsx"]
    create_modal = True
    edit_modal = True


class UserAdminView(CustomAdminView):
    column_exclude_list = ("_password",)
    column_searchable_list = ("first_name", "last_name", "is_staff", "email")
    column_filters = ("first_name", "last_name", "is_staff", "email")
    column_editable_list = ("first_name", "last_name", "is_staff")
    can_create = False
    can_edit = True
    can_delete = False


class ArticleAdminView(CustomAdminView):
    column_searchable_list = (
        "author.user.first_name",
        "author.user.last_name",
        "title",
        "tags.name",
    )
    column_hide_backrefs = False
    column_display_pk = True
    # column_select_related_list = ("author.user", "tags")
    column_list = ("id", "title", "author.user", "tags", "body")
    column_editable_list = ("tags",)
    export_types = ["csv", "xlsx"]
    can_create = False
    can_edit = True
    can_delete = True
    edit_modal = True
