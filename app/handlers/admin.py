from os import getenv
from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter#это надо для нескольких фсмок!!!!!!!!!!!!!!!!!
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram import Bot
from aiogram.types import FSInputFile
from aiogram.exceptions import AiogramError

import app.keyboards.admin as kb
import app.keyboards.main as us
from app.handlers.other_func import send_message_user, get_content_info
from datetime import datetime

class Admin(StatesGroup):
    isAdmin = State()
    mailing = State()
    set_filters = State()

uptime = datetime.now()

admin_router = Router()
LOGIN = str(getenv("LOGIN"))
PASSWORD = str(getenv("PASSWORD"))

@admin_router.message(Command('login'))
async def admin_login(message: Message, state: FSMContext):
    try:
        login = message.text.split()[1]
        password = message.text.split()[2]
    except IndexError:
        login = None
        password = None
    if login == LOGIN and password == PASSWORD:
        await message.delete()
        await state.clear()
        await state.set_state(Admin.isAdmin)
        await message.answer(f"""Вы авторизировались в админ-панель!""", reply_markup=kb.admin_main_keyboard)

@admin_router.callback_query(StateFilter(Admin.mailing, Admin.set_filters, Admin.isAdmin), F.data == "main_adm")
async def main(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    await state.set_state(Admin.isAdmin)
    await callback.message.edit_text("Вы перешли в главное меню админ-панели", reply_markup=kb.admin_main_keyboard)

@admin_router.callback_query(Admin.isAdmin, F.data == "report")
async def report(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.answer("")
        report = f"""
<b>ОТЧЕТ ПО БД</b>:

<b>🧑КОЛ-ВО ПОЛЬЗОВАТЕЛЕЙ:</b> {len(await get_ids())}
"""
        await callback.message.edit_text(report, reply_markup=kb.admin_main_keyboard)
    except AiogramError:
        pass

@admin_router.callback_query(Admin.isAdmin, F.data == "sending")
async def send_step1(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.answer("")
    await state.set_state(Admin.mailing)
    await callback.message.answer("🧾Введите текст рассылки", reply_markup=kb.go_main_admin)

@admin_router.message(Admin.mailing)
async def send_step2(message: Message, state: FSMContext, bot: Bot):
    mailing_list = await get_ids()
    count = 0
    err = 0
    for id in mailing_list:
        try:
            content = get_content_info(message)
            await send_message_user(
                bot=bot,
                user_id=id,
                content_type=content["content_type"],
                content_text=content["content_text"],
                file_id=content["file_id"],
                kb = us.start_keyboard

            )
            count += 1
        except Exception as e:
            print(e)
            err += 1
    await state.set_state(Admin.isAdmin)
    await message.answer(f'''✅Рассылка завершена
Cообщение было отправлено {count} пользователям, {err} пользователей сообщение не получили''', reply_markup=kb.admin_main_keyboard)


@admin_router.callback_query(Admin.isAdmin, F.data == "runtime")
async def report(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.answer("")
        runtime = datetime.now() - uptime
        await callback.message.edit_text(f"""⏰С момента запуска бота прошло {runtime.days} дней, {runtime.seconds // 3600} часов, {(runtime.seconds % 3600) // 60} минут, {runtime.seconds % 60} секунд""", reply_markup=kb.admin_main_keyboard)
    except AiogramError:
        pass

@admin_router.callback_query(Admin.isAdmin, F.data == "get_db")
async def main(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    recv = await get_usernames()
    if recv:
        await callback.message.answer_document(FSInputFile("database/db.txt"), caption="🗃️Сформированная БД")
        await callback.message.answer("Главное меню админ-панели", reply_markup=kb.admin_main_keyboard)
    else:
        await callback.message.answer("Произошла ошибка отправки", reply_markup=kb.admin_main_keyboard)

@admin_router.callback_query(StateFilter(Admin.isAdmin, Admin.set_filters), F.data == "filters")
async def go_filters(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Admin.isAdmin)
    await callback.answer("")
    await callback.message.edit_text(f"Вы перешли в меню фильтров", reply_markup=kb.admin_filters_menu_keyboard)


@admin_router.callback_query(Admin.isAdmin, F.data == "set_filter")
async def set_filter_step1(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    await state.set_state(Admin.set_filters)
    try:
        await callback.message.edit_text(f"""Введите фильтры (через пробел)⬇️""",reply_markup=kb.go_filters_admin)
    except AiogramError:
        pass

@admin_router.message(Admin.set_filters)
async def set_filter_step2(message: Message, state: FSMContext):
    filters = message.text
    await keys.set_filters_ru(filter=filters)
    await state.set_state(Admin.isAdmin)
    await message.answer(f"Успешно установлен фильтр на {filters}", reply_markup=kb.admin_filters_menu_keyboard)

@admin_router.callback_query(Admin.isAdmin, F.data == "set_default_filter")
async def set_filter_step1(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    await keys.set_default_filters()
    default_filters = await keys.get_current_filters()
    try:
        await callback.message.edit_text(f"""Дефолтный фильтр установлен:
{', '.join(default_filters)}
""",reply_markup=kb.admin_filters_menu_keyboard)
    except AiogramError:
        pass

@admin_router.callback_query(Admin.isAdmin, F.data == "check_filter")
async def check_filters(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    default_filters = await keys.get_current_filters()
    try:
        await callback.message.edit_text(f"""Текущий фильтр:
{', '.join(default_filters)}
""",reply_markup=kb.admin_filters_menu_keyboard)
    except AiogramError:
        pass
@admin_router.callback_query(Admin.isAdmin, F.data == "mode")
async def mode(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    await callback.message.edit_text(f"""Вы перешли в меню режима работы.

Текущий режим работы: {keys.mode}
""", reply_markup=kb.admin_mode_menu_keyboard)


@admin_router.callback_query(Admin.isAdmin, F.data == "set_mode")
async def mode(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    await keys.set_mode()
    await callback.message.edit_text(f"""Вы изменили режим работы на {keys.mode}""", reply_markup=kb.admin_mode_menu_keyboard)



