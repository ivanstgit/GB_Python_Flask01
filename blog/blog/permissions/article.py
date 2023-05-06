from combojsonapi.permission.permission_system import (
    PermissionMixin,
    PermissionUser,
    PermissionForGet,
    PermissionForPatch,
    PermissionForPost,
)
from flask_combo_jsonapi.exceptions import AccessDenied
from flask_login import current_user
from blog.models.article import Article


class ArticlePermission(PermissionMixin):
    ALL_AVAILABLE_FIELDS = [
        "id",
        "title",
        "body",
    ]

    PATCH_AVAILABLE_FIELDS = [
        "title",
        "body",
    ]

    def get(self, *args, many=True, user_permission: PermissionUser = None, **kwargs) -> PermissionForGet:  # type: ignore
        """
        Set available columns
        :param args:
        :param many:
        :param user_permission:
        :param kwargs:
        :return:
        """
        if not current_user.is_authenticated:
            raise AccessDenied("no access")

        self.permission_for_get.allow_columns = (self.ALL_AVAILABLE_FIELDS, 10)

        return self.permission_for_get

    def patch_permission(self, *args, user_permission: PermissionUser = None, **kwargs) -> PermissionForPatch:  # type: ignore
        if not current_user.is_authenticated:
            raise AccessDenied("no access")

        if current_user.is_staff:
            self.permission_for_patch.allow_columns = (self.ALL_AVAILABLE_FIELDS, 10)
        else:
            self.permission_for_patch.allow_columns = (self.PATCH_AVAILABLE_FIELDS, 10)
        return self.permission_for_patch

    def patch_data(self, *args, data: dict = None, obj: Article = None, user_permission: PermissionUser = None, **kwargs) -> dict:  # type: ignore
        permission_for_patch = user_permission.permission_for_patch_permission(model=Article)

        if obj.author.user.id == current_user.id or current_user.is_staff:
            return {
                i_key: i_val
                for i_key, i_val in data.items()
                if i_key in permission_for_patch.columns
            }
        else:
            raise AccessDenied("no access")
