from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from database.dependency.services import user_service
from tgbot.keyboards import KeyboardService
from tgbot.utils import create_translator_hub_from_directory

# Подгружаем наши переводы из файлов.
t_hub = create_translator_hub_from_directory()


class DB(BaseMiddleware):
    def __init__(self):
        super().__init__()

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Any,
            data: Dict[str, Any]
    ) -> Any:
        tg_user_model = getattr(event.message or event.callback_query, 'from_user', None)
        user_model = await user_service.get_or_create(tg_id=tg_user_model.id)

        data["i18n"] = t_hub.get_translator_by_locale('ru')
        data["t_hub"] = t_hub
        data["keyboard_service"] = KeyboardService(i18n=data['i18n'])
        data["user"] = user_model
        await handler(event, data)
