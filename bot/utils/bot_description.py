from aiogram import Bot


async def set_bot_description(bot: Bot):
    description = 'Что умеет делать этот бот?\n{bot name} - уникальный инструмент для поставщиков Wildberries, который позволяет наблюдать за продажами, практически в реальном времен, а так же строить отчеты, анализировать конкурентов и многое другое.\n{bot name} покажет все что скрыто.'
    await bot.set_my_description(description=description)