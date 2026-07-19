import os
from aiogram import F, Router
from aiogram.exceptions import AiogramError
from aiogram.types import Message, CallbackQuery, BusinessMessagesDeleted
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
from core_database.work.crud import *
from app.handlers.other_func import send_message_user, get_content_info
from aiogram import Bot
import io
from aiogram.types import BufferedInputFile


import app.keyboards.main as kb
from datetime import datetime

load_dotenv()
admin_id = int(os.getenv("ADMIN_ID"))
bot_id = int(os.getenv("BOT_ID"))
not_save = [admin_id, bot_id]
uptime = datetime.now()
main_router = Router()

@main_router.business_message()
async def hi(message: Message, bot: Bot):
    tg_id = int(message.from_user.id)
    username = message.from_user.username
    fullname = message.from_user.full_name
    message_id = message.message_id
    text = message.text or message.caption
    if text and ("⠀" in text) and (tg_id == admin_id):
        if message.reply_to_message.photo:
            file_id = message.reply_to_message.photo[-1].file_id
            photo_buffer = io.BytesIO()
            await bot.download_file(
                file_path=(await bot.get_file(file_id)).file_path,
                destination=photo_buffer
            )
            photo_buffer.seek(0)
            photo_to_send = BufferedInputFile(
                photo_buffer.getvalue(),
                filename="downloaded_photo.jpg"
            )
            await bot.send_photo(chat_id=admin_id, photo=photo_to_send, caption=
            f"""Самоуничтожающееся фото пользователя {message.reply_to_message.from_user.full_name} @{message.reply_to_message.from_user.username}""")

        elif message.reply_to_message.video:
            video_buffer = io.BytesIO()
            file_id = message.reply_to_message.video.file_id
            file = await bot.get_file(file_id)
            await bot.download_file(file.file_path, video_buffer)
            video_buffer.seek(0)
            video_to_send = BufferedInputFile(
                video_buffer.getvalue(),
                filename="processed_video.mp4"
            )
            await bot.send_video(chat_id=admin_id, video=video_to_send, caption=
            f"""Самоуничтожающееся видео пользователя {message.reply_to_message.from_user.full_name} @{message.reply_to_message.from_user.username}""")
            # file = await bot.get_file(message.reply_to_message.photo[-1].file_id)
            # ext = file.file_path.split('.')[-1] if '.' in file.file_path else 'jpg'
            # filename = f"{message_id}_{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.{ext}"
            # file_path = os.path.join("D:\\photos", filename)
            # await bot.download_file(file.file_path, file_path)

    if tg_id not in not_save:
        info = get_content_info(message)
        await create_user(tg_id=tg_id, username=username, fullname=fullname)
        await create_message(message_id=message_id, text=text, user_id=tg_id, type=info.get("content_type", ""), file_id=info.get("file_id",""))


@main_router.business_message(Command("start"))
async def hi(message: BusinessMessagesDeleted):
    print("Start message")
    
@main_router.deleted_business_messages()
async def hi(message: BusinessMessagesDeleted, bot: Bot):
    msg_list = message.message_ids
    for id in msg_list:
        msg = await get_message(message_id=id)
        if msg:
            await send_message_user(bot, user_id=admin_id, content_type=msg.type, content_text=
            f"""Пользователь {msg.user.fullname} @{msg.user.username} удалил сообщение <blockquote>{msg.text}</blockquote>""",
                                    file_id=msg.file_id)
            await delete_message(message_id=id)
@main_router.edited_business_message()
async def hi(message: Message, bot: Bot):
    old_msg = await get_message(message_id=message.message_id)
    text = message.text or message.caption
    if old_msg:
        info = get_content_info(message)
        new_msg = await create_message(message_id=message.message_id, text=text, user_id=info.from_user.id, type=info.get("content_type", ""), file_id=info.get("file_id",""))
        await bot.send_message(chat_id=admin_id, text=f"""Пользователь {old_msg.user.fullname} @{old_msg.user.username} изменил сообщение
<blockquote>{old_msg.text}</blockquote>
на
<blockquote>{new_msg.text}</blockquote>
""")

@main_router.message(Command("help"))
async def help(message: Message, bot: Bot):
    await message.answer(f"""
GhostKeeper - это телеграм-бот, который позволяет защищать сообщения в Telegram от удаления собеседником. Программа следит за удалением сообщений и отправляет вам самоуничтожающиеся медиафайлы.

Нажми на этот символ --->[<code>⠀</code>], затем вставь его в ответ на самоуничтожающееся сообщение, чтобы скачать его
""" )







