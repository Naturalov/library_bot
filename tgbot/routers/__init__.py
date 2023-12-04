from aiogram import Dispatcher

from tgbot.routers import user


async def setup_routers(dp: Dispatcher):
    dp.include_router(user.router)
