import os

API_TOKEN = os.getenv('API_TOKEN', '')
CHATTER_BOT_DB_URI = os.getenv('CHATTER_BOT_DB_URI', '')
REDIS_HOST = os.getenv('REDIS_HOST', '')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_UPDATES_CHANNEL = os.getenv('REDIS_UPDATE_CHANNEL', 'tg:update')
SENTRY_SDK_KEY = os.getenv('SENTRY_SDK_KEY', '')
STORE_PATH = os.getenv('STORE_PATH', '')
VERSION = os.getenv('VERSION', '')
VK_SECRET_KEY = os.getenv('VK_SECRET_KEY', '')
VK_CLIENT_ID = os.getenv('VK_CLIENT_ID', '')
VK_AUTH_REDIRECT_URI = 'https://rkashapov.tk/auth/callback/vk/'
BOT_USERNAME = os.getenv('BOT_USERNAME', '')
