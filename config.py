import os
import logging
import ssl

from dotenv import load_dotenv

load_dotenv()

DEBUG = bool(int(os.getenv('DEBUG', 0)))
# DATABASE_URL = os.getenv('DATABASE_URL')
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = list(map(int, os.getenv('ADMIN_ID').split(',')))

# Broker settings
# HOST = os.getenv('MQQT_BROKER')
# PORT = int(os.getenv('MQTT_PORT'))
# USERNAME = os.getenv('MQTT_USERNAME')
# PASSWORD = os.getenv('MQTT_PASSWORD')
# SSL_CONTEXT = ssl.create_default_context()

if not BOT_TOKEN:
    logging.error("BOT_TOKEN is not defined neither in .env file nor in environment variables")
    quit()
