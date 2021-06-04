from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from pymongo import MongoClient
from db import db_write, db_chek_blocklist, send_all_message, flood_control
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
    chek = db_chek_blocklist(message)
    if chek == False:
        await message.reply_text("<b>Ты заблокирован в этом боте навсегда</b>",
                                 reply_to_message_id=message.message_id)
    else:
        db_write(message)
        await message.reply_text(f"<b>Добро пожаловать, {message.from_user.mention}</b>",
                                 reply_to_message_id=message.message_id)


@Client.on_message(filters.command(["stat"], "/") & filters.all)
async def stat(client, message):
    if message.from_user.username == me_chat_id:
        db = createDB["users"]
        count = db.count_documents({})
        await message.reply_text(f"<b>Пользователей в боте: {count}</b>",
                                 reply_to_message_id=message.message_id)


@Client.on_message(filters.command(["enable_antiflood"], "/") & filters.all)
async def enable_antiflood(client, message):
    if message.from_user.username == me_chat_id \
            and len(message.text.split()) == 1:
        db = createDB["flood"]
        enable = db.find_one({"ENABLE": f"YES"})
        if enable != None:
            await message.reply_text(f"<b>[Анти-флуд] уже включен!</b>",
                                     reply_to_message_id=message.message_id)
        else:
            antifl = {"ENABLE": f"YES"}
            db.insert_one(antifl).inserted_id
            await message.reply_text(f"<b>[Анти-флуд] включен!</b>",
                                     reply_to_message_id=message.message_id)
    elif message.from_user.username == me_chat_id \
            and len(message.text.split()) == 2:
        disable = message.text.split(" ")[1]
        db = createDB["flood"]
        enable = db.find_one({"ENABLE": f"YES"})
        if enable != None \
                and disable == "disable":
            db.delete_one({"ENABLE": f"YES"})
            await message.reply_text(f"<b>[Анти-флуд] выключен!</b>",
                                     reply_to_message_id=message.message_id)
        elif enable == None \
                and disable == "disable":
            await message.reply_text(f"<b>[Анти-флуд] не включен!</b>",
                                     reply_to_message_id=message.message_id)


@Client.on_message(filters.command(["blocklist"], "/") & filters.all)
async def db_write_blocklist(client, message):
    if message.from_user.username == me_chat_id \
            and len(message.text.split()) == 2:
        message_split = message.text.split(" ")[1]
        db = createDB["block_id"]
        user = db.find_one({"USER_ID": f"{message_split}"})
        if user != None:
            await message.reply_text(f"<b>Пользователь уже добавлен в черный список бота!</b>",
                                     reply_to_message_id=message.message_id)
        else:
            db = createDB["block_id"]
            user = {"USER_ID": f"{message_split}"}
            db.insert_one(user).inserted_id
            await message.reply_text(f"<b>Пользователь добавлен в черный список бота!</b>",
                                     reply_to_message_id=message.message_id)
    elif message.from_user.username == me_chat_id \
            and len(message.text.split()) != 2:
        await message.reply_text("<b>Кого заблокировать?</b>",
                                 reply_to_message_id=message.message_id)


@Client.on_message(filters.command(["unblocklist"], "/") & filters.all)
async def db_write_unblocklist(client, message):
    if message.from_user.username == me_chat_id \
            and len(message.text.split()) == 2:
        message_split = message.text.split(" ")[1]
        db = createDB["block_id"]
        find_user_in_black = db.find_one({"USER_ID": f"{message_split}"})
        if find_user_in_black != None:
            db.delete_one({"USER_ID": f"{message_split}"})
            await message.reply_text(f"<b>Пользователь удален из черного список бота!</b>",
                                     reply_to_message_id=message.message_id)
        else:
            await message.reply_text(f"<b>Пользователь не в черном списке бота!</b>",
                                     reply_to_message_id=message.message_id)
    elif message.from_user.username == me_chat_id \
            and len(message.text.split()) != 2:
        await message.reply_text("<b>Кого разблокировать?</b>",
                                 reply_to_message_id=message.message_id)


@Client.on_message(filters.private & filters.all)
async def feedback(client, message):
    chek = db_chek_blocklist(message)
    flood = await flood_control(message)
    if message.from_user.username != me_chat_id \
            and flood != False:
        if chek == False:
            await message.reply_text("<b>Ты заблокирован в этом боте навсегда</b>",
                                     reply_to_message_id=message.message_id)
        else:
            db_write(message)
            db = createDB["message_ids"]
            if message.media_group_id != None:
                msg_find = db.find_one({"MEDIA_GROUP_ID": f"{message.media_group_id}"})
                if msg_find == None:
                    message_media_group_id = {"MEDIA_GROUP_ID": f"{message.media_group_id}"}
                    db.insert_one(message_media_group_id).inserted_id
                    msg_list = await client.get_media_group(message.chat.id, message.message_id)
                    list_ids = []
                    for _ in msg_list:
                        list_ids.append(_.message_id)
                    forward = await client.forward_messages(chat_id=me_chat_id,
                                                            from_chat_id=message.chat.id,
                                                            message_ids=list_ids)
                    message_id = ({"MESSAGE_DATE": f"{forward[0].forward_date}",
                                   "USER_ID": f"{message.from_user.id}"})
                    db.insert_one(message_id).inserted_id
                    print(f"Сообщение {message_id['MESSAGE_DATE']} добавлено в БД")
            else:
                forward = await message.forward(me_chat_id)
                message_id = ({"MESSAGE_DATE": f"{forward.forward_date}",
                            "USER_ID": f"{message.from_user.id}"})
                db.insert_one(message_id).inserted_id
                print(f"Сообщение {message_id['MESSAGE_DATE']} добавлено в БД")
    elif message.from_user.username == me_chat_id and message.reply_to_message:
        try:
            db = createDB["message_ids"]
            user_id = db.find_one({"MESSAGE_DATE": f"{message.reply_to_message.forward_date}"})
            print(f"Пользователь {user_id['USER_ID']} найден")
            if message.media_group_id != None:
                msg_find = db.find_one({"MEDIA_GROUP_ID": f"{message.media_group_id}"})
                if msg_find == None:
                    message_media_group_id = {"MEDIA_GROUP_ID": f"{message.media_group_id}"}
                    db.insert_one(message_media_group_id).inserted_id
                    await client.copy_media_group(user_id["USER_ID"],
                                                          me_chat_id,
                                                          message_id=message.message_id)
            else:
                await client.copy_message(user_id["USER_ID"],
                                        me_chat_id,
                                        message_id=message.message_id)
        except Exception as e:
            await message.reply_text(f"<b>{e}</b>",
                                     reply_to_message_id=message.message_id)

    elif message.from_user.username == me_chat_id and message.reply_to_message == None:
        promote_button = InlineKeyboardButton("Рассылать?", callback_data="promote")
        delete_button = InlineKeyboardButton("Удалить", callback_data="delete")
        promote_keyboard = InlineKeyboardMarkup([[promote_button],[delete_button]])
        if message.media_group_id != None:
            db = createDB["message_ids"]
            msg_find = db.find_one({"MEDIA_GROUP_ID": f"{message.media_group_id}"})
            if msg_find == None:
                message_media_group_id = {"MEDIA_GROUP_ID": f"{message.media_group_id}"}
                db.insert_one(message_media_group_id).inserted_id
                msg_list = await client.copy_media_group(me_chat_id,
                                                         me_chat_id,
                                                         message_id=message.message_id)
                await msg_list[1].reply_text("<b>Подтвердите рассылку медиа группы</b>",
                                             reply_markup=promote_keyboard,
                                             reply_to_message_id=msg_list[1].message_id)
        else:
            await client.copy_message(me_chat_id,
                                      me_chat_id,
                                      message_id=message.message_id,
                                      reply_markup=promote_keyboard)


@Client.on_callback_query()
async def callback_call(client, message):
    if message.data == "promote":
        if message.message.reply_to_message != None:
            await message.message.delete()
            await send_all_message(client, message)
            await message.message.reply_to_message.delete()
        else:
            await message.message.edit_reply_markup(reply_markup=ReplyKeyboardRemove())
            await send_all_message(client, message)
            await message.message.delete()
    if message.data == "delete":
        await message.message.delete()
