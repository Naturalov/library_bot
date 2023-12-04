from aiogram.filters.callback_data import CallbackData


class BookCallback(CallbackData, prefix="lc"):
    page: int = 0
    filter_status: str | None = None


class DeleteBook(CallbackData, prefix='sad'):
    id: int


class GetBook(CallbackData, prefix='das'):
    id: int
