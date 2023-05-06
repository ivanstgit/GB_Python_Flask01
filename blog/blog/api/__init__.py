from flask_combo_jsonapi import Api

api = Api()


def init_api(app):
    from combojsonapi.spec import ApiSpecPlugin
    from combojsonapi.event import EventPlugin
    from combojsonapi.permission import PermissionPlugin

    event_plugin = EventPlugin()

    api_spec_plugin = ApiSpecPlugin(
        app=app,
        tags={
            "Tag": "Tag API",
            "User": "User API",
            "Author": "Author API",
            "Article": "Article API",
        }
    )

    permission_plugin = PermissionPlugin(strict=False)

    api.plugins = [
        event_plugin,
        api_spec_plugin,
        permission_plugin
    ]

    api.init_app(app)


def register_api_routes(url_prefix):
    from blog.api.tag import TagList, TagDetail
    from blog.api.user import UserList, UserDetail
    from blog.api.author import AuthorList, AuthorDetail
    from blog.api.article import ArticleList, ArticleDetail

    api.route(TagList, "tag_list", url_prefix + "/tags/", tag="Tag")
    api.route(TagDetail, "tag_detail", url_prefix + "/tags/<int:id>/", tag="Tag")
    api.route(UserList, "user_list", url_prefix + "/users/", tag="User")
    api.route(UserDetail, "user_detail", url_prefix + "/users/<int:id>/", tag="User")
    api.route(AuthorList, "author_list", url_prefix + "/authors/", tag="Author")
    api.route(AuthorDetail, "author_detail", url_prefix + "/authors/<int:id>/", tag="Author")
    api.route(ArticleList, "article_list", url_prefix + "/aticles/", tag="Article")
    api.route(ArticleDetail, "article_detail", url_prefix + "/articles/<int:id>/", tag="Article")
