from aiogram import F, Router, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery


from bot.database.database import *
from bot.database.functions.db_requests import DbRequests
from bot.routers.chats.commands import inline_kb_selectseller
from bot.utils.states import *


chat_callbacks_router = Router()


@chat_callbacks_router.callback_query()
async def chat_callback_query_handler(callback_query: types.CallbackQuery, state: FSMContext, db_request: DbRequests):
    code = callback_query.data
    tg_id = str(callback_query.from_user.id)
    print(code)
    if 'addseller' in code:
        chat_id = str(callback_query.message.chat.id)
        
    elif 'delseller' in code:
        chat_id = None

    seller_id = code.split('_')[-1]
    upd_seller = db_request.update_seller(id=int(seller_id), update_chat=True, chat_id=chat_id)
    seller = [s for s in db_request.get_seller(user_id=db_request.get_user(tg_id=str(callback_query.from_user.id)).id) if s.is_active]
    text, reply_markup = inline_kb_selectseller(sellers=seller, chat_id=str(callback_query.message.chat.id))
    if 'addseller' in code:
        text += f"\n\nПродавец \"{upd_seller.name}\" подключен \nк данному чату (ID: {callback_query.message.chat.id})\nТеперь ежедневные уведомления будут приходить сюда."
    elif 'delseller' in code:
        text += f"\n\nПродавец \"{upd_seller.name}\" отключен \nот данного чата (ID: {callback_query.message.chat.id})\nТеперь ежедневные уведомления приходить не будут."
    await callback_query.message.edit_text(text=text, reply_markup=reply_markup)
    