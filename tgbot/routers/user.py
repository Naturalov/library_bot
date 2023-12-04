from typing import Any

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ChatJoinRequest, CallbackQuery
from fluentogram import TranslatorRunner

from database import schemas
from database.services.book_service import BookService
from database.services.user_service import UserService
from tgbot.keyboards import KeyboardService
from tgbot.utils.callback import BookCallback, GetBook, DeleteBook
from tgbot.utils.states import AddBook, BookFilter

# Инициализация роутера
router = Router(name="user")


@router.message(CommandStart())
async def send_start(message: Message,
                     i18n: TranslatorRunner,
                     keyboard_service: KeyboardService):
    await message.answer(text=i18n.get("request-message"),
                         reply_markup=keyboard_service.get_main())


@router.callback_query(BookCallback.filter())
async def send_books(event: CallbackQuery,
                     i18n: TranslatorRunner,
                     callback_data: BookCallback,
                     user: schemas.User,
                     book_service: BookService,
                     keyboard_service: KeyboardService):
    on_page = 5
    offset_book = callback_data.page * on_page
    limit_page = on_page
    books = await book_service.get_all(user_id=user.id,
                                       offset=offset_book,
                                       limit=limit_page,
                                       filter_books_query=callback_data.filter_status)

    prev_page = callback_data.page - 1 if callback_data.page > 0 else None
    next_page = callback_data.page + 1 if not len(books) < on_page else None
    await event.message.edit_text(text=i18n.get("books-menu"),
                                  reply_markup=keyboard_service.get_books(books=books,
                                                                          next_page=next_page,
                                                                          prev_page=prev_page,
                                                                          filter_status=callback_data.filter_status))


@router.callback_query(GetBook.filter())
async def fun(event: CallbackQuery,
              i18n: TranslatorRunner,
              callback_data: GetBook,
              user: schemas.User,
              book_service: BookService,
              keyboard_service: KeyboardService,
              user_service: UserService):
    book = await book_service.get(id=callback_data.id)
    await event.message.edit_text(text=i18n.get('book-preview',
                                                name=book.name,
                                                author=book.author,
                                                description=book.description,
                                                genre=book.genre),
                                  reply_markup=keyboard_service.get_delete_book(id=book.id))
    await send_start(message=event.message,
                     i18n=i18n,
                     keyboard_service=keyboard_service)


@router.callback_query(DeleteBook.filter())
async def fun(event: CallbackQuery,
              i18n: TranslatorRunner,
              callback_data: DeleteBook,
              user: schemas.User,
              book_service: BookService,
              keyboard_service: KeyboardService,
              user_service: UserService):
    await book_service.delete_book(id=callback_data.id)
    await event.message.edit_text(text=i18n.get('book-deleted'))


@router.callback_query(F.data == 'filter_book')
async def fun(event: CallbackQuery,
              i18n: TranslatorRunner,
              state: FSMContext,
              user_service: UserService):
    await event.message.edit_text(text=i18n.get('book-filter'))
    await state.set_state(BookFilter.input_filter)
    await state.update_data(event=event)


@router.message(BookFilter.input_filter)
async def fun(event: Message,
              i18n: TranslatorRunner,
              user: schemas.User,
              book_service: BookService,
              keyboard_service: KeyboardService,
              state: FSMContext,
              user_service: UserService):
    await event.delete()
    data = await state.get_data()
    prev_event: CallbackQuery = data['event']
    await send_books(event=prev_event,
                     i18n=i18n,
                     callback_data=BookCallback(filter_status=event.text),
                     user=user,
                     book_service=book_service,
                     keyboard_service=keyboard_service)


@router.callback_query(F.data == 'add_book')
async def fun(event: CallbackQuery,
              i18n: TranslatorRunner,
              state: FSMContext,
              user_service: UserService):
    await event.message.edit_text(text=i18n.get('books-add-menu'))
    await state.set_state(AddBook.input_name)


@router.message(AddBook.input_name)
async def fun(event: Message,
              i18n: TranslatorRunner,
              state: FSMContext,
              user_service: UserService):
    await state.update_data(name=event.text)
    await event.answer(text=i18n.get('books-add-author'))
    await state.set_state(AddBook.input_author)


@router.message(AddBook.input_author)
async def fun(event: Message,
              i18n: TranslatorRunner,
              state: FSMContext,
              user_service: UserService):
    await state.update_data(author=event.text)
    await event.answer(text=i18n.get('books-add-description'))
    await state.set_state(AddBook.input_description)


@router.message(AddBook.input_description)
async def fun(event: Message,
              i18n: TranslatorRunner,
              state: FSMContext,
              user_service: UserService):
    await state.update_data(description=event.text)
    await event.answer(text=i18n.get('books-add-genre'))
    await state.set_state(AddBook.input_genre)


@router.message(AddBook.input_genre)
async def fun(event: Message,
              i18n: TranslatorRunner,
              state: FSMContext,
              user: schemas.User,
              book_service: BookService,
              keyboard_service: KeyboardService,
              user_service: UserService):
    await state.update_data(genre=event.text)

    data = await state.get_data()

    book = await book_service.create(**data,
                                     user_id=user.id)

    await event.answer(text=i18n.get('book-preview',
                                     **data))
    await send_start(message=event,
                     i18n=i18n,
                     keyboard_service=keyboard_service)
    await state.clear()
