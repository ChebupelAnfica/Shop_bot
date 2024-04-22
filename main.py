import asyncio
import sys
import logging

from aiogram import Bot, Dispatcher, types, F

from aiogram.filters import Command
from handler.main.handlers import router
from database.models import async_main
from config import TOKEN
from keyboards.inlane.inlane_key import set_commands
from handler.main.pay import order, pre_check_query
from handler.main.handlers import (catalog, category_selected, cmd_start, product_selected, echo_files, cmd_clear,
                                   contact)

async def start_bot(bot: Bot):
    await set_commands(bot)


async def main():
    await async_main()

    bot = Bot(token=TOKEN, parse_mode="HTML")
    dp = Dispatcher()
    dp.message.register(cmd_start, Command('start'))
    dp.message.register(catalog, F.text == "Каталог")
    dp.message.register(cmd_clear, Command('clear'))
    dp.callback_query.register(category_selected, F.data.startswith('category_'))
    dp.callback_query.register(product_selected, F.data.startswith('product_'))
    dp.pre_checkout_query.register(pre_check_query)
    dp.message.register(order, Command("pay"))
    dp.message.register(contact)
    dp.message.register(echo_files)
    dp.startup.register(start_bot)
    await dp.start_polling(bot)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")


