from aiogram import Bot
from aiogram.types import BotCommandScopeDefault


async def set_bot_commands(bot: Bot):
    usercommands = [
    ]
    await bot.set_my_commands(usercommands, scope=BotCommandScopeDefault())

