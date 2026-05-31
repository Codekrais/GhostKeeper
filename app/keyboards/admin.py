from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, \
    inline_keyboard_markup

admin_main_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Отчет по БД📝", callback_data="report"), InlineKeyboardButton(text="Рассылка🔃", callback_data="sending"),InlineKeyboardButton(text="Получить БД🗃️", callback_data="get_db")],
    [InlineKeyboardButton(text="RUNTIME бота⏰", callback_data="runtime"), InlineKeyboardButton(text="Фильтр-меню🎛️", callback_data="filters"),InlineKeyboardButton(text="Выйти из панели⛔", callback_data="main")],
])

go_filters_admin = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="В меню фильтров🔴", callback_data="filters")],
])

go_main_admin = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="В главное меню панели🔴", callback_data="main_adm")],
])

admin_mode_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Поменять режим работы♻️", callback_data="set_mode"),InlineKeyboardButton(text="В меню фильтров🔴", callback_data="filters")],
])

admin_filters_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Установить фильтр👮‍♂️", callback_data="set_filter"),InlineKeyboardButton(text="Сбросить фильтр↩️", callback_data="set_default_filter"), InlineKeyboardButton(text="Просмотреть фильтр", callback_data="check_filter")],
    [InlineKeyboardButton(text="Режим работы бота📆", callback_data="mode")],
    [InlineKeyboardButton(text="В главное меню панели🔴", callback_data="main_adm")]
])
