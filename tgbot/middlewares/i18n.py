from typing import Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import Message
from fluentogram import TranslatorHub

from database.dependency.services import user_service
from ..utils import create_translator_hub_from_directory

# Подгружаем наши переводы из файлов.
t_hub = create_translator_hub_from_directory()


class I18nMiddleware(BaseMiddleware):
    def __init__(self, t_hub: TranslatorHub):
        self.t_hub = t_hub

    async def __call__(
            self,
            handler: Any,
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        tg_user_model = getattr(event.message or event.callback_query, 'from_user', None)
        user_model = await user_service.get_or_create(tg_id=tg_user_model.id)

        data["i18n"] = self.t_hub.get_translator_by_locale(user_model.language_code)
        data["t_hub"] = self.t_hub
        await handler(event, data)
