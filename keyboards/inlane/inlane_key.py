from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command="start",
            description="Запустить бота."
        ),
        BotCommand(
            command="pay",
            description="Оплатить заказ."
        ),
        BotCommand(
            command='clear',
            description="Очистить чат."
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())