import handlers, middlewares
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from loader import *
import logging
import asyncio


logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
                    datefmt="%d-%m-%Y %H:%M:%S")

dp.middleware.setup(LoggingMiddleware())


async def start_polling():
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(start_polling())
