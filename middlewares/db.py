from typing import Any, Awaitable, Callable
from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from sqlalchemy.ext.asyncio import async_session


class DataBaseSession(BaseMiddleware):
    def __init__(self, session_pool: async_session):
        self.session_pool = session_pool

    
    async def __call__(
            self,
            hendler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any],
    )-> Any:
        async with self.session_pool() as session:
            data['session'] = session
            return await hendler(event, data)