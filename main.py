# python modules
import asyncio
import os
# aiogram
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
# env (python-dotenv)
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())
# bot files
from hendlers.message_hendler import mrouter
from hendlers.callback_queries import cbrouter
from common.commands_menu import menu
# database
from database.engine import create_db, session_maker, drop_db
# middlewares
from middlewares.db import DataBaseSession
# temporarily decision
from functions.update_prices import schedule_price_update

ALLOWED_UPDATES = ['message', 'edited_message', 'callback_query']


bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()


dp.include_router(mrouter)  # message router
dp.include_router(cbrouter)  # callback router


async def start(bot):
    drop=False
    if drop:
        await drop_db()
    await create_db()

async def stop(bot):
    print('bot has turned off')


async def main():
    dp.startup.register(start)
    dp.shutdown.register(stop)

    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=menu, scope=types.BotCommandScopeAllPrivateChats())

    # start task "update prices"
    asyncio.create_task(schedule_price_update())

    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)



if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('bot has turned off\n"KeyboardInterrupt"')
