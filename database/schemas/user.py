from database.models.user import PermissionEnum
from database.schemas.base import SchemaBase


class User(SchemaBase):
    id: int
    tg_id: int
    username: str | None
    permission: PermissionEnum
    language_code: str | None
