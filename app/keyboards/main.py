from aiogram.filters import callback_data
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
start_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Инструкция📝", url="https://telegra.ph/GAJD-PO-NASTROJKEC-02-26")],
    [InlineKeyboardButton(text="VPN 🔧", callback_data="get_vpn_keys"), InlineKeyboardButton(text="WHITE V1🔧", callback_data="get_zieng_keys"),InlineKeyboardButton(text="WHITE V2🔧", callback_data="get_white_keys")],
    [InlineKeyboardButton(text="Поддержка🤝", url="https://t.me/codebykrais?direct")]

])

