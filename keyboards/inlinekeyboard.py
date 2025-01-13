from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder



def tags_list(TrackList):
    builder = InlineKeyboardBuilder()
    for tag in TrackList:
        builder.button(text=tag, callback_data=tag)
    builder.adjust(1)
    return builder.as_markup()
