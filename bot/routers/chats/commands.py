import asyncio

from aiogram.types import Message
from aiogram import Router
from aiogram.filters import Command
from aiogram.utils.formatting import Code
from aiogram.fsm.context import FSMContext
from aiogram.enums.parse_mode import ParseMode

import logging

from bot.database.database import *
from bot.database.functions.db_requests import DbRequests
from bot.keyboards import *
from bot.wildberries import *
from bot.utils.states import *
from bot.utils.abc_analysis import get_abc

chat_commands_router = Router()

def inline_kb_selectseller(sellers, chat_id):
    text = "Выберите продавцов, которых хотите добавить в чат.\n✅ отмечены уже добавленные"
    text_and_data = []
    for seller in sellers:
        if seller.chat_id == chat_id and chat_id != None:
            text_and_data.append([f"✅ {seller.name}", f"delseller_{seller.id}"])
        elif seller.chat_id != chat_id or seller.chat_id == None:
            text_and_data.append([f"{seller.name}", f"addseller_{seller.id}"])
    reply_markup = InlineConstructor.create_kb(text_and_data=text_and_data)
    return text, reply_markup
        
@chat_commands_router.message(Command("connect"))
async def cmd_create(message: Message, db_request: DbRequests):
    seller = [s for s in db_request.get_seller(user_id=db_request.get_user(tg_id=str(message.from_user.id)).id) if s.is_active]
    if len(seller) == 0:
        await message.answer("У вас нет активных продавцов, пополните счет и подключите продавцов в личном кабинете бота.")
    elif len(seller) == 1:
        db_request.update_seller(id=seller[0].id, chat_id=str(message.chat.id), update_chat=True)
        await message.answer(f"Продавец \"{seller[0].name}\" подключен к данному чату (ID: {message.chat.id}).\nТеперь ежедневные уведомления будут приходить сюда.")
    else:
        text, reply_markup = inline_kb_selectseller(sellers=seller, chat_id=str(message.chat.id))
        await message.answer(text=text, reply_markup=reply_markup)