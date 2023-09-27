from aiogram.types import Message
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.enums.parse_mode import ParseMode

from bot.database.database import *
from bot.database.functions.db_requests import DbRequests
from bot.keyboards import *
from bot.utils.states import *

admin_commands_router = Router()


@admin_commands_router.message(Command("admin"))
async def cmd_admin(message: Message, db_request: DbRequests):
    text, reply_markup = inline_kb_admin(db_request)
    await message.answer(text=text, reply_markup=reply_markup)
