from database import models, schemas


class Constructors:
    @staticmethod
    def construct_book_schema_by_model(book: models.Book) -> schemas.Book:
        return schemas.Book(id=book.id,
                            name=book.name,
                            author=book.author,
                            description=book.description,
                            genre=book.genre)
