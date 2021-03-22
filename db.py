from pymongo import MongoClient
import configparser
import sys
import os
config_path = os.path.join(sys.path[0], 'config.ini')
config = configparser.ConfigParser()
config.read(config_path)
MongoDB = config.get('anime_girl', 'db_url')
connectDB = MongoClient(MongoDB)
createDB = connectDB.feedback_bot


def db_write(message):
    try:
        db = createDB["users"]
        user = db.find_one({"USER_ID": f"{message.chat.id}"})["USER_ID"]
        print(f"Ползователь {user} уже добавлен в БД")
    except:
        db = createDB["users"]
        user = {"USER_ID": f"{message.chat.id}",
                "FIRST_NAME": f"{message.from_user.first_name}",}
        db.insert_one(user).inserted_id
        print(f"Ползователь {user['USER_ID']} добавлен в БД")


def db_chek_blocklist(message):
    db = createDB["block_id"]
    user = db.find_one({"USER_ID": f"{message.chat.id}"})["USER_ID"]
    print(f"Пользователь {user} забанен в боте")