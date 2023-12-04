from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fluentogram import TranslatorRunner

from database import schemas
from tgbot.utils.callback import GetBook, BookCallback, DeleteBook


class UserKeyboardService:
    def __init__(self,
                 i18n: TranslatorRunner):
        self.i18n: TranslatorRunner = i18n

    def get_main(self) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.row(InlineKeyboardButton(text=self.i18n.get('kb-books'),
                                         callback_data=BookCallback().pack()))
        return builder.as_markup()

    def get_books(self,
                  books: list[schemas.Book],
                  next_page: int | None = None,
                  prev_page: int | None = None,
                  filter_status: str | None = None) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        for book in books:
            builder.row(InlineKeyboardButton(text=self.i18n.get('kb-book',
                                                                name=book.name,
                                                                author=book.author),
                                             callback_data=GetBook(id=book.id).pack()))
        builder.row(InlineKeyboardButton(text=self.i18n.get('kb-prev-page'), callback_data=BookCallback(
            page=prev_page,
            filter_status=filter_status).pack()) if prev_page is not None else InlineKeyboardButton(
            text=self.i18n.get('kb-none-page'),
            callback_data='強'),
                    InlineKeyboardButton(text=self.i18n.get('kb-book-add'),
                                         callback_data='add_book'),
                    InlineKeyboardButton(text=self.i18n.get('kb-next-page'), callback_data=BookCallback(
                        page=next_page,
                        filter_status=filter_status).pack()) if next_page is not None else InlineKeyboardButton(
                        text=self.i18n.get('kb-none-page'),
                        callback_data='強'))
        builder.row(InlineKeyboardButton(text=self.i18n.get('kb-filter'),
                                         callback_data='filter_book'))
        return builder.as_markup()

    def get_delete_book(self,
                        id: int) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.row(InlineKeyboardButton(text=self.i18n.get('kb-delete'),
                                         callback_data=DeleteBook(id=id).pack()))
        return builder.as_markup()
