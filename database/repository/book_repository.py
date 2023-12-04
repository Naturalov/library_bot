from tortoise.expressions import Q

from database import models


class BookRepository:

    def __init__(self) -> None:
        ...

    @staticmethod
    async def get(id: int) -> models.Book:
        q_id = Q(id=id) if id else Q()
        return await models.Book.filter(q_id).first()

    @staticmethod
    async def create(user_id: int,
                     name: str,
                     author: str,
                     description: str,
                     genre: str) -> models.Book:
        return await models.Book.create(user_id=user_id,
                                        name=name,
                                        author=author,
                                        description=description,
                                        genre=genre)

    @staticmethod
    async def get_all(user_id: int,
                      filter_books_query: str | None = None,
                      offset: int | None = None,
                      limit: int | None = None) -> list[models.Book]:
        q_user_id = Q(user__id=user_id) if user_id else Q()
        q_filter_books_query = Q(name__icontains=filter_books_query) | Q(author__icontains=filter_books_query) | Q(
            description__icontains=filter_books_query) if filter_books_query else Q()
        books_query = models.Book.filter(q_user_id,
                                         q_filter_books_query)
        if offset: books_query = books_query.offset(offset=offset)
        if limit: books_query = books_query.limit(limit=limit)

        return await books_query.all()

    @staticmethod
    async def delete_book(id: int) -> None:
        await models.Book.filter(id=id).delete()
