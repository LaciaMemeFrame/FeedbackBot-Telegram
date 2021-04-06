from pymongo import MongoClient
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


