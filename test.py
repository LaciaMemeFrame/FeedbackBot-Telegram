from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import requests
import asyncio
import configparser
import sys
import os
import random

BLOCK_ID = [213123132]
ADMIN_NAME = ['имя админа', 'имя админа']
ADM_CHAT_ID = [айди админа бота]
ADMIN_CHAT_ID = ['айди админа бота', 'айди админа бота']
ADMIN_BOT = [айди бота]
config_path = os.path.join(sys.path[0], 'settings.ini')
config = configparser.ConfigParser()
config.read(config_path)
BOT_TOKEN = config.get('Bot', 'BOT_TOKEN')
chat_ids_file = config.get('Bot', 'chat_ids_file')
api_id = config.get('Bot', 'api_id')
api_hash = config.get('Bot', 'api_hash')
CATAPI = config.get('Bot', 'CATAPI')
DOGAPI = config.get('Bot', 'DOGAPI')
users_amount = [0]

bot = Client("my_bot", bot_token=BOT_TOKEN, api_id=api_id, api_hash=api_hash)

def save_chat_id(chat_id):
	chat_id = str(chat_id)
	with open(chat_ids_file,"a+") as ids_file:
		ids_file.seek(0)

		ids_list = [line.split('\n')[0] for line in ids_file]

		if chat_id not in ids_list:
			ids_file.write(f'{chat_id}\n')
			ids_list.append(chat_id)
			print(f'Новый пользователь сохранен в БД: {chat_id}')
		else:
			print(f'Пользователь {chat_id} уже сохранен в БД')
		users_amount[0] = len(ids_list)
	return

def send_message_users(message):

	def send_message(chat_id):
		data = {
			'chat_id': chat_id,
			'text': message
		}
		response = requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage', data=data)

	with open(chat_ids_file, "r") as ids_file:
		ids_list = [line.split('\n')[0] for line in ids_file]

	[send_message(chat_id) for chat_id in ids_list]

@bot.on_message(filters.command(["help"], "/") & filters.all)
async def help(bot, message):
    if message.chat.id in BLOCK_ID:
        return
    await bot.send_message(message.chat.id, text = f"<b>Все команды бота!\n/help - Все команды бота\n/dogs - Собачки с thedogapi.com\n/kitty - Котики с thecatapi.com\n/wallpaper - Аниме обои с nekos.life</b>", parse_mode="HTML", disable_notification=True, reply_to_message_id=message.message_id)

@bot.on_message(filters.command(["idsed"], "/"))
async def text(bot, message):
    if message.chat.id not in ADM_CHAT_ID:
        return
    if message.chat.id in ADM_CHAT_ID:
        try:
            ids = message.text.split(" ", maxsplit=2)[1]
        except Exception as e:
                    await bot.send_message(message.chat.id, text = f"<b>{e}</b>", parse_mode='HTML', reply_to_message_id=message.message_id)
        await asyncio.sleep(0.5)
        try:
            mess = message.text.split(" ", maxsplit=2)[2]
        except Exception as e:
                    await bot.send_message(message.chat.id, text = f"<b>{e}</b>", parse_mode='HTML', reply_to_message_id=message.message_id)
        await asyncio.sleep(0.5)
        try:
            await bot.send_message(ids, text = f"{mess}", disable_notification=True, reply_to_message_id=message.message_id, parse_mode = 'HTML')
            await bot.send_message(message.chat.id, text = f"<a href='tg://user?id={random.choice(ADMIN_CHAT_ID)}'>Ваше сообщение</a> <code>{mess}</code> успешно отправленно <a href='tg://user?id={ids}'>пользователю</a>", disable_notification=True, reply_to_message_id=message.message_id, parse_mode = 'HTML')
        except Exception as e:
                    await bot.send_message(message.chat.id, text = f"<b>{e}</b>", parse_mode='HTML', reply_to_message_id=message.message_id)
        await asyncio.sleep(0.5)




@bot.on_message(filters.command(["wallpaper"], "/") & filters.all)
async def wallpaper(bot, message):
    if message.chat.id in BLOCK_ID:
        return
    URL = f"https://nekos.life/api/v2/img/wallpaper"
    r = requests.get(URL, allow_redirects=True)
    r.headers
    json = r.json()
    loveurl = json['url']
    reply_makup = InlineKeyboardButton
    try:
        await bot.send_photo(message.chat.id, loveurl, reply_to_message_id=message.message_id, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Скачать в высоком качестве', url=f'{loveurl}')]]))
    except Exception as e:
                await bot.send_message(message.chat.id, text = f"<b>{e}</b>", parse_mode='HTML', reply_to_message_id=message.message_id)
    await asyncio.sleep(0.5)

@bot.on_message(filters.command(["dogs"], "/") & filters.all)
async def dogs(bot, message):
    if message.chat.id in BLOCK_ID:
        return
    URL = f"https://api.thedogapi.com/v1/images/search"
    r = requests.get(URL, allow_redirects=True)
    r.headers['x-api-key'] = DOGAPI
    json = r.json()
    for j in json:
        dogsurl = j['url']
        reply_makup = InlineKeyboardButton
        try:
            await bot.send_photo(message.chat.id, dogsurl, reply_to_message_id=message.message_id, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Скачать в высоком качестве', url=f'{dogsurl}')]]))
        except Exception as e:
                    await bot.send_message(message.chat.id, text = f"<b>{e}</b>", parse_mode='HTML', reply_to_message_id=message.message_id)
        await asyncio.sleep(0.5)

@bot.on_message(filters.command(["kitty"], "/") & filters.all)
async def kitty(bot, message):
    if message.chat.id in BLOCK_ID:
        return
    URL = f"https://api.thecatapi.com/v1/images/search"
    r = requests.get(URL, allow_redirects=True)
    r.headers['x-api-key'] = DOGAPI
    json = r.json()
    for j in json:
        kittyurl = j['url']
        reply_makup = InlineKeyboardButton
        try:
            await bot.send_photo(message.chat.id, kittyurl, reply_to_message_id=message.message_id, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Скачать в высоком качестве', url=f'{kittyurl}')]]))
        except Exception as e:
                    await bot.send_message(message.chat.id, text= f"<b>{e}</b>", parse_mode='HTML', reply_to_message_id=message.message_id)
        await asyncio.sleep(0.5)

@bot.on_message(filters.command(["start"], "/") & filters.all)
async def start(bot, message):
    await bot.send_message(message.chat.id, f"<b>Добро пожаловать, {message.from_user.first_name}</b>", parse_mode='HTML', disable_notification=True, reply_to_message_id=message.message_id)
    save_chat_id(message.chat.id)

@bot.on_message(filters.command(["stat"], "/") & filters.all)
async def stat(bot, message):
    if message.chat.id in ADM_CHAT_ID:
        await bot.send_message(message.chat.id, text = f"<b>Статистика пользователей!\nПользователей: {users_amount[0]}</b>", parse_mode='HTML', disable_notification=True, reply_to_message_id=message.message_id)

@bot.on_message(filters.command(["ads"], "/") & filters.all)
async def stat(bot, message):
    if message.chat.id in ADM_CHAT_ID:
        msg = message.text.replace("/ads ", "")
        send_message_users(msg) 
        await bot.send_message(message.chat.id, text = f"<b>сообщение успешно отправлено всем ({users_amount[0]}) пользователям бота!</b>", parse_mode='HTML', disable_notification=True)


@bot.on_message(filters.private & filters.all)
async def stic(bot, message):
    if message.chat.id in BLOCK_ID:
        return
    if message.from_user.id in ADM_CHAT_ID:
        return
    if message.from_user.id in ADMIN_BOT:
        return
    if  message.text != None:
        await bot.send_message(random.choice(ADMIN_CHAT_ID), text = f"Имя - {message.from_user.first_name}\nid - <code>{message.from_user.id}</code>\n<a href='tg://user?id={message.from_user.id}'>Permalink</a>\nТекст сообщения - {message.text}", disable_notification=True)
        await bot.send_message(message.chat.id, text = f"<b>Ваше сообщение успешно доставлено пользователю <a href='tg://user?id={random.choice(ADMIN_CHAT_ID)}'>{random.choice(ADMIN_NAME)}</a></b>", disable_notification=True, reply_to_message_id=message.message_id)
    elif message.text == None:
        try:
            try:
                await bot.send_sticker(random.choice(ADMIN_CHAT_ID), sticker = f"{message.sticker.file_id}", disable_notification=True)
                await bot.send_message(random.choice(ADMIN_CHAT_ID), text = f"Имя - {message.from_user.first_name}\nid - <code>{message.from_user.id}</code>\n<a href='tg://user?id={message.from_user.id}'>Permalink</a>", disable_notification=True)
            except: 
                try:
                    await bot.send_document(random.choice(ADMIN_CHAT_ID), document = f"{message.document.file_id}", caption = f"Имя - {message.from_user.first_name}\nid - <code>{message.from_user.id}</code>\n<a href='tg://user?id={message.from_user.id}'>Permalink</a>", disable_notification=True)
                except:
                    try:
                        await bot.send_photo(random.choice(ADMIN_CHAT_ID), photo = f"{message.photo.file_id}", caption = f"Имя - {message.from_user.first_name}\nid - <code>{message.from_user.id}</code>\n<a href='tg://user?id={message.from_user.id}'>Permalink</a>", disable_notification=True)
                    except:
                        try:
                            await bot.send_audio(random.choice(ADMIN_CHAT_ID), audio = f"{message.audio.file_id}", caption = f"Имя - {message.from_user.first_name}\nid - <code>{message.from_user.id}</code>\n<a href='tg://user?id={message.from_user.id}'>Permalink</a>", disable_notification=True)
                        except: 
                            await bot.send_animation(random.choice(ADMIN_CHAT_ID), animation = f"{message.animation.file_id}", caption = f"Имя - {message.from_user.first_name}\nid - <code>{message.from_user.id}</code>\n<a href='tg://user?id={message.from_user.id}'>Permalink</a>", disable_notification=True)
            await bot.send_message(message.chat.id, text = f"<b>Ваше сообщение успешно доставлено пользователю <a href='tg://user?id={random.choice(ADMIN_CHAT_ID)}'>{random.choice(ADMIN_NAME)}</a></b>", disable_notification=True, reply_to_message_id=message.message_id)
        except Exception as e:
                    await bot.send_message(message.chat.id, text = f"<b>{e}</b>", parse_mode='HTML')
        await asyncio.sleep(0.5)

bot.run()
