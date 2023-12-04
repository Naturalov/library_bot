from tortoise import Tortoise

from config_reader import config


async def init_database():
    await Tortoise.init({
        'connections': {
            'default': config.DATABASE_DNS
        },
        "apps": {
            "models": {
                "models": ["database.models"],
                "default_connection": "default",
            },
        },
    })
    await Tortoise.generate_schemas()
