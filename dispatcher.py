from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN

default = DefaultBotProperties(parse_mode='MARKDOWN')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
