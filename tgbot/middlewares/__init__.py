from aiogram import Dispatcher

from .db import DB
from .i18n import I18nMiddleware, t_hub


async def setup_middlewares(dp: Dispatcher):
    dp.update.outer_middleware(DB())
    dp.update.outer_middleware(I18nMiddleware(t_hub))
