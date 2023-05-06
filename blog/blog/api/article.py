from flask_combo_jsonapi import ResourceDetail, ResourceList
from combojsonapi.event.resource import EventsResource
from blog.permissions.article import ArticlePermission

from blog.schemas import ArticleSchema
from blog.models.database import db
from blog.models import Article


class ArticleListEvents(EventsResource):
    def event_get_count(self):
        return {"count": Article.query.count()}


class ArticleList(ResourceList):
    schema = ArticleSchema
    data_layer = {
        "session": db.session,
        "model": Article,
    }
    events = ArticleListEvents


class ArticleDetail(ResourceDetail):
    schema = ArticleSchema
    data_layer = {
        "session": db.session,
        "model": Article,
        "permission_patch": [ArticlePermission],
    }
