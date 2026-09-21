import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from handler import router1
from aiogram.types import BotCommand
import os
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv("bot_token")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=bot_token)
dp = Dispatcher()

dp.include_router(router1)


async def main():
    print("Бот запущен и ждёт сообщений...")
    commands = [
        BotCommand(command="menu", description="Menu")
    ]
    await bot.set_my_commands(commands)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())