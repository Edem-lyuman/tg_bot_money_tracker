from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup,
                           InlineKeyboardButton)

from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_users




async def handle_users():
    all_users = await get_users()
    keyboard = InlineKeyboardBuilder()

    for user in all_users:
        keyboard.add(InlineKeyboardButton(text=str(user.tg_id), callback_data='user_' + str(user.id)))

    return keyboard.adjust(2).as_markup()


