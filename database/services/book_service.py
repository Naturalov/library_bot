from database import schemas
from database.repository.book_repository import BookRepository
from database.services.constructors import Constructors


class BookService:
    def __init__(self,
                 constructors: Constructors,
                 book_repository: BookRepository):
        self._constructors = constructors
        self._book_repository = book_repository

    async def get(self,
                  id: int) -> schemas.Book:
        book = await self._book_repository.get(id=id)
        return self._constructors.construct_book_schema_by_model(book=book)

    async def create(self,
                     user_id: int,
                     name: str,
                     author: str,
                     description: str,
                     genre: str) -> schemas.Book:
        book = await self._book_repository.create(user_id=user_id,
                                                  name=name,
                                                  author=author,
                                                  description=description,
                                                  genre=genre)

        return self._constructors.construct_book_schema_by_model(book=book)

    async def get_all(self,
                      user_id: int,
                      filter_books_query: str | None = None,
                      offset: int | None = None,
                      limit: int | None = None) -> list[schemas.Book]:
        books = await self._book_repository.get_all(user_id=user_id,
                                                    filter_books_query=filter_books_query,
                                                    offset=offset,
                                                    limit=limit)

        return [self._constructors.construct_book_schema_by_model(book=book) for book in books]

    async def delete_book(self,
                          id: int) -> None:
        await self._book_repository.delete_book(id=id)
