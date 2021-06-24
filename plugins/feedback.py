from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, Message
from pyrogram.errors import UserBlocked
from utils.db import db_write, db_chek_blocklist, send_all_message, flood_control, me_chat_id, users, blocklist, flood, \
    message_ids, media_group_id


@Client.on_message(filters.command(["start"]) & ~filters.edited)
async def start(client: Client, message: Message):
    chek = await db_chek_blocklist(message)
    if not chek:
        await message.reply_text("<b>Ты заблокирован в этом боте навсегда</b>",
                                 reply_to_message_id=message.message_id)
    else:
        await db_write(message)
        await message.reply_text(f"<b>Добро пожаловать, {message.from_user.mention}</b>",
                                 reply_to_message_id=message.message_id)


@Client.on_message(filters.command(["stat"]) & ~filters.edited)
async def stat(client: Client, message: Message):
    if message.from_user.username == me_chat_id:
        count = await users.count_documents({})
        await message.reply_text(f"<b>Пользователей в боте: {count}</b>",
                                 reply_to_message_id=message.message_id)


@Client.on_message(filters.command(["enable_antiflood"]) & ~filters.edited)
async def enable_antiflood(client: Client, message: Message):
    if message.from_user.username == me_chat_id \
            and len(message.text.split()) == 1:
        enable = await flood.find_one({"ENABLE": f"YES"})
        if enable:
            await message.reply_text(f"<b>[Анти-флуд] уже включен!</b>",
                                     reply_to_message_id=message.message_id)
        else:
            antifl = {"ENABLE": f"YES"}
            await flood.insert_one(antifl)
            await message.reply_text(f"<b>[Анти-флуд] включен!</b>",
                                     reply_to_message_id=message.message_id)
    elif message.from_user.username == me_chat_id \
            and len(message.text.split()) == 2:
        disable = message.text.split(" ")[1]
        enable = await flood.find_one({"ENABLE": f"YES"})
        if enable \
                and disable == "disable":
            await flood.delete_one({"ENABLE": f"YES"})
            await message.reply_text(f"<b>[Анти-флуд] выключен!</b>",
                                     reply_to_message_id=message.message_id)
        elif enable is None \
                and disable == "disable":
            await message.reply_text(f"<b>[Анти-флуд] не включен!</b>",
                                     reply_to_message_id=message.message_id)


@Client.on_message(filters.command(["ban"]) & ~filters.edited)
async def db_write_blocklist(client: Client, message: Message):
    if message.from_user.username == me_chat_id \
            and message.reply_to_message:
        find_user = await message_ids.find_one({"MESSAGE_ID": f"{message.reply_to_message.message_id}"})
        user = await blocklist.find_one({"USER_ID": f"{find_user['USER_ID']}"})
        if user:
            await message.reply_text(f"<b>Пользователь уже добавлен в черный список бота!</b>",
                                     reply_to_message_id=message.message_id)
        else:
            add_user = {"USER_ID": f"{find_user['USER_ID']}"}
            await blocklist.insert_one(add_user)
            await message.reply_text(f"<b>Пользователь добавлен в черный список бота!</b>",
                                     reply_to_message_id=message.message_id)
    elif message.from_user.username == me_chat_id \
            and not message.reply_to_message:
        await message.reply_text("<b>Кого заблокировать?</b>",
                                 reply_to_message_id=message.message_id)


@Client.on_message(filters.command(["unban"]) & ~filters.edited)
async def db_write_unblocklist(client: Client, message: Message):
    if message.from_user.username == me_chat_id \
            and message.reply_to_message:
        find_user = await message_ids.find_one({"MESSAGE_ID": f"{message.reply_to_message.message_id}"})
        user = await blocklist.find_one({"USER_ID": f"{find_user['USER_ID']}"})
        if user:
            await blocklist.delete_one({"USER_ID": f"{find_user['USER_ID']}"})
            await message.reply_text(f"<b>Пользователь разбанен!</b>",
                                     reply_to_message_id=message.message_id)
        else:
            await message.reply_text(f"<b>Пользователь не забанен!</b>",
                                     reply_to_message_id=message.message_id)
    elif message.from_user.username == me_chat_id \
            and not message.reply_to_message:
        await message.reply_text("<b>Кого разблокировать?</b>",
                                 reply_to_message_id=message.message_id)


@Client.on_message(filters.private & filters.all & ~filters.edited)
async def feedback(client: Client, message: Message):
    chek = await db_chek_blocklist(message)
    flood = await flood_control(message)
    if message.from_user.username != me_chat_id \
            and flood != False:
        if not chek:
            if message.media_group_id:
                media_group = await media_group_id(message)
                if media_group != False:
                    await message.reply_text("<b>Ты заблокирован в этом боте навсегда</b>",
                                             reply_to_message_id=message.message_id)
            else:
                await message.reply_text("<b>Ты заблокирован в этом боте навсегда</b>",
                                             reply_to_message_id=message.message_id)
        else:
            await db_write(message)
            if message.media_group_id:
                media_group = await media_group_id(message)
                if media_group != False:
                    forward = await client.forward_messages(chat_id=me_chat_id,
                                                            from_chat_id=message.chat.id,
                                                            message_ids=[_.message_id for _ in
                                                                         await client.get_media_group
                                                                         (message.chat.id,
                                                                          message.message_id)])
                    for _, i in zip([_.message_id for _ in await client.get_media_group
                        (message.chat.id,
                         forward[0].message_id)],
                                    [_.message_id for _ in await client.get_media_group
                                        (message.chat.id,
                                         message.message_id)]):
                        message_id = ({"MESSAGE_ID": f"{_}",
                                       "USER_ID": f"{message.from_user.id}",
                                       "REPLY_MESSAGE_ID": f"{i}"})
                        await message_ids.insert_one(message_id)
            else:
                forward = await message.forward(me_chat_id)
                message_id = ({"MESSAGE_ID": f"{forward.message_id}",
                               "USER_ID": f"{message.from_user.id}",
                               "REPLY_MESSAGE_ID": f"{message.message_id}"})
                await message_ids.insert_one(message_id)
    elif message.from_user.username == me_chat_id \
            and message.reply_to_message:
        try:
            user_id = await message_ids.find_one({"MESSAGE_ID": f"{message.reply_to_message.message_id}"})
            if message.media_group_id:
                media_group = await media_group_id(message)
                if media_group != False:
                    await client.copy_media_group(user_id["USER_ID"],
                                                  me_chat_id,
                                                  message_id=message.message_id,
                                                  reply_to_message_id=int(user_id["REPLY_MESSAGE_ID"]))
                    await message.reply_text(
                        f"<b>Вы успешно отправили сообщение <a href='tg://user?id={user_id['USER_ID']}'>пользоватлю</a></b>")
            else:
                await client.copy_message(user_id["USER_ID"],
                                          me_chat_id,
                                          message_id=message.message_id,
                                          reply_to_message_id=int(user_id["REPLY_MESSAGE_ID"]))
                await message.reply_text(
                    f"<b>Вы успешно отправили сообщение <a href='tg://user?id={user_id['USER_ID']}'>пользоватлю</a></b>")
        except UserBlocked as e:
            await message.reply_text(f"<b>{e}</b>",
                                     reply_to_message_id=message.message_id)

    elif message.from_user.username == me_chat_id and not message.reply_to_message:
        promote_button = InlineKeyboardButton("Рассылать?", callback_data="promote")
        delete_button = InlineKeyboardButton("Удалить", callback_data="delete")
        promote_keyboard = InlineKeyboardMarkup([[promote_button], [delete_button]])
        if message.media_group_id:
            media_group = await media_group_id(message)
            if media_group != False:
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
        if message.message.reply_to_message:
            await message.message.delete()
            await send_all_message(client, message)
            await client.delete_messages(message.message.chat.id,
                                         [_.message_id for _ in await client.get_media_group
                                         (message.message.chat.id,
                                          message.message.reply_to_message.message_id)])
        else:
            await message.message.edit_reply_markup(reply_markup=ReplyKeyboardRemove())
            await send_all_message(client, message)
            await message.message.delete()
    if message.data == "delete":
        if message.message.reply_to_message:
            await client.delete_messages(message.message.chat.id,
                                         [_.message_id for _ in await client.get_media_group
                                         (message.message.chat.id,
                                          message.message.reply_to_message.message_id)])
            await message.message.delete()
        else:
            await message.message.delete()
