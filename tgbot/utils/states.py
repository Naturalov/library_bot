from aiogram.fsm.state import StatesGroup, State


class AddBook(StatesGroup):
    input_name = State()
    input_author = State()
    input_description = State()
    input_genre = State()


class BookFilter(StatesGroup):
    input_filter = State()
