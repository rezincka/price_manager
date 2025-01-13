from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def taglist():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Кнопка 1")
    builder.button(text="Кнопка 2")
    builder.adjust(2)  # Упорядочить в 2 столбца
    return builder.as_markup()