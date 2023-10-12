import asyncio
import logging
import sys
from os import getenv
import requests

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold

# Bot token can be obtained via https://t.me/BotFather
TOKEN = "6370860035:AAGW0BaYxeYfJPLXWbHBHPLd6A6TgXPnGXU"

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer("Please enter a vacancy")


@dp.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    await message.answer("Это бот для поиска работы по Украине. Для начала поиска введите команду start и придерживайтесь дальнейших указаний")


@dp.message()
async def message_handler(message: types.Message) -> None:
    vac = message.text
    params = {'keyWords': vac}
    response = requests.get('https://api.rabota.ua/vacancy/search', params=params)
    resp: dict = response.json()
    documents_list: list = resp['documents']
    for i in range(len(documents_list)):
        vac_name = documents_list[i]["name"], documents_list[i]["cityName"]
        await message.answer(str(vac_name))


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

