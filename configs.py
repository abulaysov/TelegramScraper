from telethon import TelegramClient
import os
import dotenv

dotenv.load_dotenv()


LIST_CHANNELS = os.getenv('LIST_CHANNELS').split()
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')

client = TelegramClient('my_account', API_ID, API_HASH)
