from pymongo import MongoClient
import configparser
import sys
import os
from asyncio import sleep
from time import time
from collections import defaultdict
from typing import Union

config_path = os.path.join(sys.path[0], 'config.ini')
config = configparser.ConfigParser()
config.read(config_path)
me_chat_id = config.get('anime_girl', 'chat_id')
MongoDB = config.get('anime_girl', 'db_url')
connectDB = MongoClient(MongoDB)
createDB = connectDB.feedback_bot
USERS = defaultdict(list)
MESSAGES = 10
SECONDS = 5


def db_write(message):
    db = createDB["users"]
    user = db.find_one({"USER_ID": f"{message.chat.id}"})
    if user != None:
        print(f"Ползователь {user['USER_ID']} уже добавлен в БД")
    else:
        user = {"USER_ID": f"{message.chat.id}",
                "FIRST_NAME": f"{message.from_user.first_name}", }
        db.insert_one(user).inserted_id
        print(f"Ползователь {user['USER_ID']} добавлен в БД")


def db_chek_blocklist(message):
    db = createDB["block_id"]
    user = db.find_one({"USER_ID": f"{message.chat.id}"})
    if user != None:
        print(f"Пользователь {user['USER_ID']} забанен в боте")
        return False
    else:
        return True


async def send_all_message(client, message):
    db = createDB["users"]
    count = 0
    for users in db.find():
        await sleep(6)
        try:
            if message.message.reply_to_message != None:
                await client.copy_media_group(users["USER_ID"],
                                              me_chat_id,
                                              message_id=message.message.reply_to_message.message_id)
            else:
                await client.copy_message(users["USER_ID"],
                                          me_chat_id,
                                          message_id=message.message.message_id)
            count += 1
        except:
            pass
    await message.message.reply_text(f"<b>Сообщение успешно разослано {count} пользователям</b>")


async def isFlood(message: int) -> Union[bool, None]:
    USERS[message.from_user.id].append(time())
    if len(list(filter(lambda x: time() - int(x) < SECONDS, USERS[message.from_user.id]))) > MESSAGES:
        return False


async def flood_control(message):
    if await isFlood(message) is False:
        db_chek_antiflood = createDB["flood"]
        chek_antiflood = db_chek_antiflood.find_one({"ENABLE": "YES"})
        if chek_antiflood != None:
            print("flood")
            db = createDB["block_id"]
            user = db.find_one({"USER_ID": f"{message.from_user.id}"})
            if user != None \
                    and message.from_user.username != me_chat_id:
                print("[ФЛУД] Пользователь уже добавлен в черный список бота!")
                await message.reply_text("<b>Ты заблокирован в этом боте навсегда</b>",
                                         reply_to_message_id=message.message_id)
            elif user == None \
                    and message.from_user.username != me_chat_id:
                db = createDB["block_id"]
                user = {"USER_ID": f"{message.from_user.id}"}
                db.insert_one(user).inserted_id
                print("[ФЛУД] Пользователь добавлен в черный список бота!")
                await message.reply_text("<b>Ты заблокирован в этом боте навсегда</b>",
                                         reply_to_message_id=message.message_id)
                return False
        else:
            return True
    else:
        db_chek_antiflood = createDB["flood"]
        chek_antiflood = db_chek_antiflood.find_one({"ENABLE": "YES"})
        if message.from_user.username != me_chat_id \
                and chek_antiflood != None:
            print("non flood")
            return True
        else:
            return True
