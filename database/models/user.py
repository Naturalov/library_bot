from enum import IntFlag, auto

from tortoise import fields
from tortoise.models import Model


class PermissionEnum(IntFlag):
    user = auto()
    worker = auto()
    moder = auto()
    admin = auto()


class User(Model):
    tg_id = fields.BigIntField(unique=True)
    username = fields.CharField(max_length=255, null=True)

    permission = fields.IntEnumField(PermissionEnum, default=PermissionEnum.user)
    language_code = fields.CharField(max_length=4,
                                     default='en')
