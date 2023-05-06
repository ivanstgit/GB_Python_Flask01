from flask_admin import Admin

from blog import models
from blog.models.database import db
from blog.views.admin.views import (
    ArticleAdminView,
    CustomAdminIndexView,
    CustomAdminView,
    TagAdminView,
    UserAdminView,
)


# Create admin with custom base template
admin = Admin(
    name="Blog Admin", index_view=CustomAdminIndexView(), template_mode="bootstrap4"
)

# Add views
admin.add_view(TagAdminView(models.Tag, db.session, category="Models"))
admin.add_view(UserAdminView(models.User, db.session, category="Models"))
admin.add_view(ArticleAdminView(models.Article, db.session, category="Models"))
