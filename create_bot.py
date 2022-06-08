import asyncio

from aiogram import Bot, Dispatcher
from config_tg.config import tg_bot_token

loop = asyncio.get_event_loop()
bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot, loop=loop)


