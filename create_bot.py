import asyncio

from aiogram import Bot, Dispatcher
from config_tg.config import tg_bot_token
# from aiogram.contrib.fsm_storage.memory import MemoryStorage

# storage=MemoryStorage()
loop = asyncio.get_event_loop()
bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot,loop=loop)
# dp = Dispatcher(bot, storage=storage)

