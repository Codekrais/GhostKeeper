import os
from aiogram import F, Router
from aiogram.exceptions import AiogramError
from aiogram.types import Message, CallbackQuery, BusinessMessagesDeleted
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
from core_database.work.crud import *
from app.handlers.other_func import send_message_user
from aiogram import Bot

import app.keyboards.main as kb
from datetime import datetime



load_dotenv()
admin_id = int(os.getenv("ADMIN_ID"))
bot_id = int(os.getenv("BOT_ID"))
not_save = [admin_id, bot_id]
uptime = datetime.now()
main_router = Router()

@main_router.business_message()
async def hi(message: Message):
    tg_id = int(message.from_user.id)
    username = message.from_user.username
    fullname = message.from_user.full_name
    message_id = message.message_id
    text = message.text
    if tg_id not in not_save:
        await create_user(tg_id=tg_id, username=username, fullname=fullname)
        await create_message(message_id=message_id, text=text, user_id=tg_id)

@main_router.business_message(Command("start"))
async def hi(message: BusinessMessagesDeleted):
    print("Start message")
    
@main_router.deleted_business_messages()
async def hi(message: BusinessMessagesDeleted, bot: Bot):
    msg_list = message.message_ids
    for id in msg_list:
        msg = await get_message(message_id=id)
        if msg:
            await bot.send_message(chat_id=admin_id, text=f"""Пользователь {msg.user.fullname} @{msg.user.username} удалил сообщение <blockquote>{msg.text}</blockquote>""")
            await delete_message(message_id=id)
@main_router.edited_business_message()
async def hi(message: Message, bot: Bot):
    old_msg = await get_message(message_id=message.message_id)
    new_msg = await create_message(message_id=message.message_id, text=message.text, user_id=message.from_user.id)
    await bot.send_message(chat_id=admin_id, text=f"""Пользователь {old_msg.user.fullname} @{old_msg.user.username} изменил сообщение
<blockquote>{old_msg.text}</blockquote> на <blockquote>{new_msg.text}</blockquote>
""")







