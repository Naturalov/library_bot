import logging

import betterlogging as bl
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Создаем экземпляр таймера по Московскому времени.
scheduler = AsyncIOScheduler()

# Загружаем логгер.
logger = logging.getLogger(__name__)
log_level = logging.INFO
bl.basic_colorized_config(level=log_level)
