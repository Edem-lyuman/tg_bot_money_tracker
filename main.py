import asyncio
import os
from aiogram import Bot, Dispatcher

from app.handlers import router
from app.database.models import async_main

from dotenv import load_dotenv

load_dotenv()


async def main():
    await async_main()
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())