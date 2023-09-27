from aiogram.types import Message
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.enums.parse_mode import ParseMode

from bot.database.database import *
from bot.database.functions.db_requests import DbRequests
from bot.keyboards import *
from bot.utils.states import *

user_commands_router = Router()

@user_commands_router.message(Command(commands=["start", "my"]))
async def cmd_start(message: Message, db_request: DbRequests, state: FSMContext):
    user = db_request.get_user(tg_id=str(message.from_user.id))
    if db_request.user_seller_exists(user_id=user.id):
        text, reply_markup = inline_kb_my(db_request, tg_id=str(message.from_user.id))
        await message.answer(text=text, reply_markup=reply_markup)
    else:
        if message.text in ['/start', '/my']:
            text, reply_markup = inline_kb_start()
            await message.answer(text=text, reply_markup=reply_markup)

        else:
            if 'addemployee' in message.text:
                seller_id = int(message.text.strip('/start ').split('_')[2])
                db_request.update_seller(id=seller_id, user_id=user.id)
                await message.answer('✅ Поздравляем! Успешное подключение.\n🥷🏻 {bot name} работает на вас 🤜🏻')
                text, reply_markup = inline_kb_add_employee(db_request, seller_id=seller_id, tg_id=str(message.from_user.id))
                await message.answer(text=text, reply_markup=reply_markup)
    await message.delete()

@user_commands_router.message(Command("balance"))
async def cmd_balance(message: Message, db_request: DbRequests):
    text, reply_markup = inline_kb_balance(db_request, tg_id=str(message.from_user.id))
    await message.answer(text=text, reply_markup=reply_markup)
    await message.delete()

@user_commands_router.message(Command("tariff"))
async def cmd_tariff(message: Message):
    text, reply_markup = inline_kb_tariff()
    await message.answer(text=text, reply_markup=reply_markup)
    await message.delete()

@user_commands_router.message(Command("news"))
async def cmd_news(message: Message, db_request: DbRequests):
    news_ids = [n.id for n in db_request.get_news()]
    if news_ids:
        text, reply_markup = inline_kb_news(db_request, news_id=news_ids[-1], tg_id=str(message.from_user.id))
    else:
        text, reply_markup = inline_kb_news(db_request, tg_id=str(message.from_user.id))
    await message.answer(text=text, reply_markup=reply_markup)
    await message.delete()

