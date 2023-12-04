from tortoise import fields, Model


class Book(Model):
    name = fields.CharField(max_length=255)
    author = fields.CharField(max_length=255)
    description = fields.CharField(max_length=255)
    genre = fields.CharField(max_length=255)
    user = fields.ForeignKeyField('models.User')
