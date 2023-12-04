from database.schemas.base import SchemaBase


class Book(SchemaBase):
    id: int
    name: str
    author: str
    description: str
    genre: str
