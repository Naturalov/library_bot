from tortoise import run_async

from database import init_database
from main import scheduler
from tgbot.misc import setup_bot

if __name__ == '__main__':
    run_async(init_database())
    scheduler.start()
    setup_bot()
