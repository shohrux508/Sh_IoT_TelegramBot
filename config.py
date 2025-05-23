import os
import logging
import ssl

from dotenv import load_dotenv

load_dotenv()

DEBUG = bool(int(os.getenv('DEBUG', 0)))
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = list(map(int, os.getenv('ADMIN_ID').split(',')))
LOCAL_HOST = os.getenv('LOCAL_HOST')
PUB_HOST = os.getenv('PUB_HOST')
host = os.getenv('host')
if int(host) == 2:
    url = PUB_HOST
else:
    url = LOCAL_HOST

if not BOT_TOKEN:
    logging.error("BOT_TOKEN is not defined neither in .env file nor in environment variables")
    quit()
