from motor.motor_asyncio import AsyncIOMotorClient
from config import *
from aiogram.contrib.fsm_storage.mongo import MongoStorage
from aiogram import Bot, Dispatcher


connectDB = AsyncIOMotorClient(DATABASE_URL)
createDB = connectDB[f"{DATABASE_FSM_NAME}"]
users = createDB.users
msg_ids = createDB.msg_ids
storage = MongoStorage(host=DATABASE_HOST_FSM,
                       db_name=DATABASE_FSM_NAME,
                       port=DATABASE_PORT_FSM,
                       username=DATABASE_USERNAME_FSM,
                       password=DATABASE_PASSWORD_FSM)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot,
                storage=storage,
                run_tasks_by_default=True)