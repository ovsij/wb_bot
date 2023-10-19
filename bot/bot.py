from aiogram import Bot

from bot.config import Config, load_config

config: Config = load_config('.env')
bot = Bot(token=config.bot.token, parse_mode='HTML', disable_web_page_preview=True)