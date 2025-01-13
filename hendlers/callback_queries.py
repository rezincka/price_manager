import asyncio
from functions.product import Product
from aiogram import Router, types, F
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession


cbrouter = Router()

# @mrouter.message(F.text.startswith('#'))
@cbrouter.callback_query()
async def tag(callback: types.CallbackQuery, session: AsyncSession):
    tag = callback.data.strip()
    price_list = await Product(
        user_id=callback.from_user.id,
        tag=tag,
    ).get_price(session)
    price_list = price_list[0]
    await callback.message.answer(f"{price_list}")
    await callback.answer()

    await callback.message.delete()