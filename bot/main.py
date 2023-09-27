import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram import F

import os
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)


from bot.config import Config, load_config
from bot.middlewares.db_session import DbSessionMiddleware
from bot.utils.bot_commands import set_commands
from bot.utils.bot_description import set_bot_description


logger = logging.getLogger(__name__)
config: Config = load_config('.env')
bot = Bot(token=config.bot.token, parse_mode='HTML', disable_web_page_preview=True)

async def on_startup(dispatcher: Dispatcher):
    config: Config = dispatcher.workflow_data["config"]
    
    dispatcher.update.middleware.register(DbSessionMiddleware())

    from bot import routers

    routers.register_all_routes(dispatcher, config)

# Запуск бота
async def main():
    logging.basicConfig(level=logging.INFO)
    logger.info('Starting Bot')
    
    dp = Dispatcher()
    dp.workflow_data.update(
        config=config,
    )

    await set_commands(bot, config)
    await set_bot_description(bot)

    dp.startup.register(on_startup)
    
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        logging.warning("Bot polling is stopped.")

#if __name__ == "__main__":
#    try:
#        asyncio.run(main())
#    except (KeyboardInterrupt, SystemExit):
#        logging.info("Bot stopped")