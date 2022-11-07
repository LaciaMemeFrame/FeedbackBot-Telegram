from middlewares.i18n import _
from loader import dp, bot, users, msg_ids
from config import *
from aiogram import types
import asyncio


@dp.message_handler(commands=['start'], commands_prefix=prefixes)
@dp.throttled(rate=rate)
async def start(msg: types.Message):
    user = await users.find_one({"id": msg.chat.id})
    if not user:
        await users.insert_one(msg.chat.to_python())
    await msg.answer(_("Привет, {}!\n"
                     "Напиши мне свой вопрос и я отвечу в течении суток").format(msg.from_user.mention))


@dp.message_handler(chat_type=types.ChatType.PRIVATE, content_types=types.ContentTypes.ANY)
@dp.throttled(rate=rate)
async def echo(msg: types.Message):
    user = await users.find_one({"id": msg.from_user.id})
    if user:
        if msg.from_user.id != ADMIN_CHAT_ID:
            msg_id = await msg.forward(ADMIN_CHAT_ID)
            await msg_ids.insert_one({"msg_id": msg_id.message_id,
                                      "user_id": msg.from_user.id,
                                      "reply_msg_id": msg.message_id})
        else:
            if msg.reply_to_message:
                search_msg = await msg_ids.find_one({"msg_id": msg.reply_to_message.message_id})
                if search_msg:
                    try:
                        try:
                            await msg.copy_to(search_msg['user_id'],
                                              reply_to_message_id=search_msg['reply_msg_id'])
                        except:
                            await msg.copy_to(search_msg['user_id'])
                    except:
                        await msg.answer(_('Пользователь заблокировал бота!'))

                else:
                    await msg.answer(_("Пользователь не найден"))
            else:
                count = 0
                async for user in users.find():
                    try:
                        await msg.copy_to(user['id'])
                        count += 1
                    except:
                        pass
                delete = await msg.answer(_("Сообщение разослано в {} чатах").format(count))
                await asyncio.sleep(1.5)
                await delete.delete()
    else:
        await msg.answer(_('Для корректной работы необходимо нажать на /start'))