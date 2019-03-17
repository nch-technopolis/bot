import os

WEBHOOK_PATH = '/bot/webhook/'
API_TOKEN = os.getenv('API_TOKEN', '')
VERSION = os.getenv('VERSION', '')
LOG_FILE_PATH = '/var/log/bot.log'

