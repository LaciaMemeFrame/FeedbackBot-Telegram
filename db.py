from pymongo import MongoClient
import configparser
import sys
import os
from time import time

config_path = os.path.join(sys.path[0], 'config.ini')
config = configparser.ConfigParser()
config.read(config_path)
me_chat_id = config.get('anime_girl', 'chat_id')
MongoDB = config.get('anime_girl', 'db_url')
connectDB = MongoClient(MongoDB)
createDB = connectDB.feedback_bot
flooders = {}
MESSAGES = 3
SECONDS = 3

def db_write(message):
    db = createDB["users"]
    user = db.find_one({"USER_ID": f"{message.chat.id}"})
    if user != None:
        print(f"Ползователь {user['USER_ID']} уже добавлен в БД")
    else:
        user = {"USER_ID": f"{message.chat.id}",
                "FIRST_NAME": f"{message.from_user.first_name}",}
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
        try:
            await client.copy_message(users["USER_ID"],
                                      me_chat_id,
                                      message_id=message.message.message_id)
            count += 1
        except:
            pass
    await message.message.reply_text(f"<b>Сообщение успешно разослано {count} пользователям</b>")


async def isFlood(message):
    message = str(message)

    try:
        flooders[message].append(time())
    except:
        flooders[message] = []
        flooders[message].append(time())

    for i in flooders[message]:
        flooders[message] = list(filter(lambda x: time() - int(x) < SECONDS, flooders[message]))

        if len(flooders[message]) > MESSAGES:
            return True
        else:
            return False


async def flood_control(message):
    if await isFlood(11):
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


