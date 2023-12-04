from aiogram import Dispatcher

from database.dependency import services


async def setup_dji(dp: Dispatcher):
    dp['user_service'] = services.user_service
    dp['book_service'] = services.book_service
