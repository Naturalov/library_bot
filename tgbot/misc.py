import logging

from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import TokenBasedRequestHandler, setup_application, SimpleRequestHandler
from aiohttp import web

from config_reader import config
from database.dependency import setup_dji
from tgbot.middlewares import setup_middlewares
from tgbot.routers import setup_routers

BOT_ENDPOINT = '/webhook/lolz_bot'


async def start_up(dispatcher: Dispatcher,
                   bot: Bot):
    await setup_dji(dispatcher)
    await setup_middlewares(dispatcher)
    await setup_routers(dispatcher)
    await bot.delete_webhook()
    await bot.set_webhook(f"{config.DOMAIN}{BOT_ENDPOINT}".format(bot_token=bot.token))


def setup_bot():
    storage = MemoryStorage()
    bot_settings = {"parse_mode": ParseMode.HTML}
    bot = Bot(token=config.bot_token, **bot_settings)
    dp = Dispatcher(storage=storage)
    dp.startup.register(start_up)
    logging.getLogger('apscheduler.executors.default').setLevel(logging.WARNING)
    logging.getLogger('aiogram.event').setLevel(logging.WARNING)

    app = web.Application()
    SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        bot_settings=bot_settings
    ).register(app, path=BOT_ENDPOINT)
    setup_application(app, dp, bot=bot)
    web.run_app(app, host='localhost', port=3435,
                print=logging.info)
