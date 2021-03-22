from pyrogram import Client
import configparser
import sys
import os

config_path = os.path.join(sys.path[0], 'config.ini')
config = configparser.ConfigParser()
config.read(config_path)
BOT_TOKEN = config.get('anime_girl', 'bot_token')
api_id = config.get('anime_girl', 'api_id')
api_hash = config.get('anime_girl', 'api_hash')
plugins = dict(root="plugins")

аниме_девочка = Client("anime_girl", bot_token=BOT_TOKEN, api_id=api_id, api_hash=api_hash, plugins=plugins)

аниме_девочка.run()
