from database.dependency.repository import user_repository, book_repository
from database.services.book_service import BookService
from database.services.constructors import Constructors
from database.services.user_service import UserService

constructors = Constructors()
user_service = UserService(user_repository=user_repository)
book_service = BookService(book_repository=book_repository,
                           constructors=constructors)
