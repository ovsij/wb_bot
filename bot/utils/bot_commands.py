from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat, BotCommandScopeAllPrivateChats

from bot.config import Config
from bot.database.functions.db_requests import DbRequests



async def set_commands(
        bot: Bot,
        config: Config
) -> None:
    commands = [
        BotCommand(
            command="my",
            description="🟢 Личный кабинет"
        ),
        BotCommand(
            command="stock",
            description="📦 Товары и остатки"
        ),
        BotCommand(
            command="search",
            description="🔍 Проверка товара в поиске"
        ),
        BotCommand(
            command="reports",
            description="📊 Отчеты"
        ),
        BotCommand(
            command="export",
            description="📁 Экспорт в таблицы"
        ),
        BotCommand(
            command="tariff",
            description="💰 Тарифы"
        ),
        BotCommand(
            command="balance",
            description="💳 Баланс"
        ),
        BotCommand(
            command="news",
            description="📜 Новости"
        ),
    ]
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeAllPrivateChats())
    db_requests = DbRequests()
    for admin in db_requests.get_user(is_admin=True):
        try:
            commands.append(
                BotCommand(
                    command="admin",
                    description="Меню администратора"
                )
            )
            await bot.set_my_commands(commands=commands, scope=BotCommandScopeChat(chat_id=admin))
        except:
            print(admin)


"""
my - 🟢 Личный кабинет
stock - 📦 Товары и остатки
search - 🔍 Проверка товара в поиске
reports - 📊 Отчеты
export - 📁 Экспорт в таблицы
tariff - 💰 Тарифы
balance - 💳 Баланс
news - 📜 Новости
"""