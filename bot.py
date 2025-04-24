import asyncio
import logging
import os
from datetime import datetime

import pytz

from config import BOT_TOKEN, DEBUG
from dispatcher import bot, dp
from modules.admin.handlers.admin import admin_rt
from modules.device_control.handlers.control_devices import devices_rt
from services.database.engine import init_db, async_session
from services.database.requests import Devices


# from tests.db_tests import start_test



def start_logging():
    if DEBUG:
        logging.basicConfig(level=logging.INFO)
        return

    if not os.path.isdir('logs'):
        os.mkdir('logs')
    logging.basicConfig(
        filename=f'./logs/bot_{BOT_TOKEN.split(":")[0]}.log',
        level=logging.INFO,
        format='~%(asctime)s %(message)s',
        encoding='utf-8'
    )

def setup_routers():
    dp.include_router(admin_rt)
    dp.include_router(devices_rt)

def setup_timezone():
    pytz.timezone("Asia/Tashkent")
    datetime.utcnow().replace(tzinfo=pytz.utc)



async def main():
    setup_routers()
    # await start_test()
    await init_db()
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    start_logging()

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
