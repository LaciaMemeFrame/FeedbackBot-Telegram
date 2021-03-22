from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient
from db import db_write, db_chek_blocklist
import asyncio
import requests
import configparser
import sys
import os

config_path = os.path.join(sys.path[0], 'config.ini')
config = configparser.ConfigParser()
config.read(config_path)
me_chat_id = config.get('anime_girl', 'chat_id')
MongoDB = config.get('anime_girl', 'db_url')
connectDB = MongoClient(MongoDB)
createDB = connectDB.feedback_bot


@Client.on_message(filters.command(["start"], "/") & filters.all)
async def start(client, message):
    delete_button = InlineKeyboardButton(f"Понятно ❌", callback_data="delete")
    delete_keyboard = InlineKeyboardMarkup([[delete_button]])
    try:
        db_chek_blocklist(message)
        await message.reply_text("<b>Ты заблокирован в этом боте навсегда</b>",
                                 reply_to_message_id=message.message_id,
                                 reply_markup=delete_keyboard)
    except:
        db_write(message)
        await message.reply_text(f"<b>Добро пожаловать, {message.from_user.mention}</b>",
                                 reply_to_message_id=message.message_id,
                                 reply_markup=delete_keyboard)


@Client.on_message(filters.command(["help"], "/") & filters.all)
async def help(client, message):
    delete_button = InlineKeyboardButton(f"Понятно ❌", callback_data="delete")
    delete_keyboard = InlineKeyboardMarkup([[delete_button]])
    try:
        db_chek_blocklist(message)
        await message.reply_text("<b>Ты заблокирован в этом боте навсегда</b>",
                                 reply_to_message_id=message.message_id,
                                 reply_markup=delete_keyboard)
    except:
        db_write(message)
        await message.reply_text("<b>Все команды бота!\n"
                                 "/help - Все команды бота\n"
                                 "/dogs - Собачки с nekos.life\n"
                                 "/kitty - Котики с nekos.life\n"
                                 "/wallpaper - Аниме обои с nekos.life</b>",
                                 reply_to_message_id=message.message_id,
                                 reply_markup=delete_keyboard)


@Client.on_message(filters.command(["stat"], "/") & filters.all)
async def stat(client, message):
    delete_button = InlineKeyboardButton(f"Понятно ❌", callback_data="delete")
    delete_keyboard = InlineKeyboardMarkup([[delete_button]])
    if message.from_user.username == me_chat_id:
        db = createDB["users"]
        count = db.count_documents({})
        await message.reply_text(f"<b>Пользователей в боте: {count}</b>",
                                reply_to_message_id=message.message_id,
                                 reply_markup=delete_keyboard)


@Client.on_message(filters.command(["wallpaper"], "/") & filters.all)
async def wallpaper(client, message):
    delete_button = InlineKeyboardButton(f"Понятно ❌", callback_data="delete")
    delete_keyboard = InlineKeyboardMarkup([[delete_button]])
    try:
        db_chek_blocklist(message)
        await message.reply_text("<b>Ты заблокирован в этом боте навсегда</b>",
                                 reply_to_message_id=message.message_id,
                                 reply_markup=delete_keyboard)
    except:
        db_write(message)
        URL = f"https://nekos.life/api/v2/img/wallpaper"
        r = requests.get(URL,
                         allow_redirects=True)
        r.headers
        json = r.json()
        loveurl = json['url']
        wallpaper_button = InlineKeyboardButton('Скачать в высоком качестве',
                                                url=f'{loveurl}')
        wallpaper_keyboard = InlineKeyboardMarkup([[wallpaper_button], [delete_button]])
        try:
            await message.reply_photo(photo=loveurl,
                                      reply_to_message_id=message.message_id,
                                      reply_markup=wallpaper_keyboard)
        except Exception as e:
            await message.reply_text(text=f"<b>{e}</b>",
                                     reply_to_message_id=message.message_id,
                                     reply_markup=delete_keyboard)
        await asyncio.sleep(0.5)


@Client.on_message(filters.command(["dogs"], "/") & filters.all)
async def dogs(client, message):
    delete_button = InlineKeyboardButton(f"Понятно ❌", callback_data="delete")
    delete_keyboard = InlineKeyboardMarkup([[delete_button]])
    try:
        db_chek_blocklist(message)
        await message.reply_text("<b>Ты заблокирован в этом боте навсегда</b>",
                                 reply_to_message_id=message.message_id,
                                 reply_markup=delete_keyboard)
    except:
        db_write(message)
        URL = f"https://nekos.life/api/v2/img/woof"
        r = requests.get(URL,
                         allow_redirects=True)
        r.headers
        json = r.json()
        dogs = json['url']
        dogs_button = InlineKeyboardButton('Скачать в высоком качестве',
                                           url=f'{dogs}')
        dogs_keyboard = InlineKeyboardMarkup([[dogs_button], [delete_button]])
        try:
            await message.reply_photo(photo=dogs,
                                      reply_to_message_id=message.message_id,
                                      reply_markup=dogs_keyboard)
        except Exception as e:
            await message.reply_text(text=f"<b>{e}</b>",
                                     reply_to_message_id=message.message_id,
                                     reply_markup=delete_keyboard)
        await asyncio.sleep(0.5)


@Client.on_message(filters.command(["kitty"], "/") & filters.all)
async def kitty(client, message):
    delete_button = InlineKeyboardButton(f"Понятно ❌", callback_data="delete")
    delete_keyboard = InlineKeyboardMarkup([[delete_button]])
    try:
        db_chek_blocklist(message)
        await message.reply_text("<b>Ты заблокирован в этом боте навсегда</b>",
                                 reply_to_message_id=message.message_id,
                                 reply_markup=delete_keyboard)
    except:
        db_write(message)
        URL = f"https://nekos.life/api/v2/img/meow"
        r = requests.get(URL,
                         allow_redirects=True)
        r.headers
        json = r.json()
        kitty = json['url']
        kitty_button = InlineKeyboardButton('Скачать в высоком качестве',
                                            url=f'{kitty}')
        kitty_keyboard = InlineKeyboardMarkup([[kitty_button], [delete_button]])
        try:
            await message.reply_photo(photo=kitty,
                                      reply_to_message_id=message.message_id,
                                      reply_markup=kitty_keyboard)
        except Exception as e:
            await message.reply_text(text=f"<b>{e}</b>",
                                     reply_to_message_id=message.message_id,
                                     reply_markup=delete_keyboard)
        await asyncio.sleep(0.5)


@Client.on_message(filters.command(["blocklist"], "/") & filters.all)
async def db_write_blocklist(client, message):
    delete_button = InlineKeyboardButton(f"Понятно ❌", callback_data="delete")
    delete_keyboard = InlineKeyboardMarkup([[delete_button]])
    if message.from_user.username == me_chat_id and len(message.text.split()) == 2:
        message_split = message.text.split(" ")[1]
        try:
            db = createDB["block_id"]
            user = db.find_one({"USER_ID": f"{message_split}"})["USER_ID"]
            await message.reply_text(f"<b>Пользователь уже добавлен в черный список бота!</b>",
                                         reply_to_message_id=message.message_id,
                                     reply_markup=delete_keyboard)
        except:
            db = createDB["block_id"]
            user = {"USER_ID": f"{message_split}"}
            db.insert_one(user).inserted_id
            await message.reply_text(f"<b>Пользователь добавлен в черный список бота!</b>",
                                     reply_to_message_id=message.message_id,
                                     reply_markup=delete_keyboard)
    elif len(message.text.split()) != 2:
        await message.reply_text("<b>Кого заблокировать?</b>",
                                 reply_to_message_id=message.message_id,
                                 reply_markup=delete_keyboard)


@Client.on_message(filters.command(["unblocklist"], "/") & filters.all)
async def db_write_unblocklist(client, message):
    delete_button = InlineKeyboardButton(f"Понятно ❌", callback_data="delete")
    delete_keyboard = InlineKeyboardMarkup([[delete_button]])
    if message.from_user.username == me_chat_id and len(message.text.split()) == 2:
        message_split = message.text.split(" ")[1]
        try:
            db = createDB["block_id"]
            db.find_one({"USER_ID": f"{message_split}"})["USER_ID"]
            db.delete_one({"USER_ID": f"{message_split}"})
            await message.reply_text(f"<b>Пользователь удален из черного список бота!</b>",
                                    reply_to_message_id=message.message_id,
                                     reply_markup=delete_keyboard)
        except:
            await message.reply_text(f"<b>Пользователь не в черном списке бота!</b>",
                                     reply_to_message_id=message.message_id,
                                     reply_markup=delete_keyboard)
    elif len(message.text.split()) != 2:
        await message.reply_text("<b>Кого разблокировать?</b>",
                                 reply_to_message_id=message.message_id,
                                 reply_markup=delete_keyboard)


@Client.on_message(filters.private & filters.all)
async def feedback(client, message):
    delete_button = InlineKeyboardButton(f"Понятно ❌", callback_data="delete")
    delete_keyboard = InlineKeyboardMarkup([[delete_button]])
    if message.from_user.username != me_chat_id:
        try:
            db_chek_blocklist(message)
            await message.reply_text("<b>Ты заблокирован в этом боте навсегда</b>",
                                     reply_to_message_id=message.message_id,
                                     reply_markup=delete_keyboard)
        except:
            db_write(message)
            forward = await message.forward(me_chat_id)
            db = createDB["message_ids"]
            message_id = ({"MESSAGE_DATE": f"{forward.forward_date}",
                           "USER_ID": f"{message.from_user.id}"})
            db.insert_one(message_id).inserted_id
            print(f"Сообщение {message_id['MESSAGE_DATE']} добавлено в БД")
            await client.send_message(me_chat_id,
                                      f"<b>Имя: {message.from_user.first_name}\n"
                                      f"ID: {message.from_user.id}\n"
                                      f"Permalink: {message.from_user.mention}</b>")
            await message.reply_text("<b>Ваше сообщение доставлено аниме-девочке!)\n\n"
                                     "Я скоро отвечу)))</b>",
                                     reply_to_message_id=message.message_id,
                                     reply_markup=delete_keyboard)
    elif message.from_user.username == me_chat_id and message.reply_to_message:
        try:
            db = createDB["message_ids"]
            user_id = db.find_one({"MESSAGE_DATE": f"{message.reply_to_message.forward_date}"})
            print(f"Пользователь {user_id['USER_ID']} найден")
            await client.copy_message(user_id["USER_ID"],
                                      me_chat_id,
                                      message_id=message.message_id,
                                      reply_markup=delete_keyboard)
            user = await client.get_users(user_id["USER_ID"])
            await message.reply_text("<b>Ваше сообщение доставлено пользователю "
                                     f"{user.mention}</b>",
                                     reply_to_message_id=message.message_id,
                                     reply_markup=delete_keyboard)
        except Exception as e:
            await message.reply_text(f"<b>{e}</b>",
                                     reply_to_message_id=message.message_id,
                                     reply_markup=delete_keyboard)

    elif message.from_user.username == me_chat_id and message.reply_to_message == None:
        db = createDB["users"]
        count = 0
        for users in db.find():
            try:
                await client.copy_message(users["USER_ID"],
                                          me_chat_id,
                                          message_id=message.message_id,
                                          reply_markup=delete_keyboard)
                count += 1
            except:
                 pass
        await message.reply_text(f"<b>Сообщение успешно разослано {count} пользователям</b>",
                                 reply_to_message_id=message.message_id,
                                 reply_markup=delete_keyboard)


@Client.on_callback_query()
async def callback(client, message):
    if message.data == "delete":
        await message.message.delete()

