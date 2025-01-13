import asyncio

from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, CommandObject

from database.models import TrackList
from functions.product import Product
from keyboards.inlinekeyboard import tags_list

from sqlalchemy.ext.asyncio import AsyncSession

mrouter = Router()
HELP_TEXT = """
Description:
that bot help you traking your goods online
(Amazon, Aliexpress, Worten, Wildberries, eBay, Ozon, Steam)

Commands list:
/start -- starting the bot
/help -- get help
/notice "yes" or "no" -- switch on and off notification
/ls -- show track list (all tags of goods, that you are tracking)
tag -- show price chart
/track tag <url> -- add new good to track list
/rm #tag -- remove good from track list
"""

@mrouter.message(CommandStart())
async def start(message: types.Message):
    await message.answer('bot start')


@mrouter.message(Command('help'))
async def start(message: types.Message):
    await message.answer(HELP_TEXT)


@mrouter.message(Command('tracklist'))
async def start(message: types.Message, session: AsyncSession):
    # Product.show_all(session=session, user_id=message.from_user.id)
    keyboard = tags_list(
        await Product.show_all(session=session, user_id=message.from_user.id))
    await message.answer('Track list:', reply_markup=keyboard)


@mrouter.message(Command('track'))
async def track(message: types.Message, session: AsyncSession, command: CommandObject):
    if command.args:
        args = command.args.split()
        print(args)
        if len(args) == 2:
            print(message.from_user.id)
            await Product(
                user_id=message.from_user.id,
                tag=args[0],
                link=args[1],
            ).add(session)
            await message.answer('has added')
    else:
        await message.answer('no arguments')
    
    


@mrouter.message(Command('remove'))
async def remove(message: types.Message, session: AsyncSession, command: CommandObject):
    if command.args:
        print(command.args)
        print(message.from_user.id)
        await Product(
            user_id=message.from_user.id,
            tag=command.args,
        ).remove(session)
        await message.answer('has removed')
    else:
        await message.answer('no arguments')


@mrouter.message()
async def get_price_list(message: types.Message, session: AsyncSession):
        tag = message.text.strip()
        price_list = await Product(
            user_id=message.from_user.id,
            tag=tag,
        ).get_price(session)
        price_list = price_list[0]
        await message.answer(f"{price_list}")



