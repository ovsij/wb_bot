from aiogram.types import Message
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.enums.parse_mode import ParseMode

from bot.database.database import *
from bot.database.functions.db_requests import DbRequests
from bot.keyboards import *
from bot.utils.states import *
from bot.wildberries import *

admin_messages_router = Router()

@admin_messages_router.message(Form.sending)
async def get_sending(message: Message, db_request: DbRequests, state: FSMContext):
    text = message.text
    await state.update_data(text=text)
    data = await state.get_data()

    text_and_data = [
        ['✅ Отправить всем', 'admin_sending_accept_all'],
        ['✅ Отправить неактивным пользователям', 'admin_sending_accept_new'],
        ['❌ Отменить', 'admin_delete_msg']
    ]
    reply_markup = InlineConstructor.create_kb(text_and_data=text_and_data)
    await message.answer(text, reply_markup=reply_markup)
    await message.delete()
    await data['message'].delete()
    
@admin_messages_router.message(Form.admin)
async def get_addadmin(message: Message, db_request: DbRequests, state: FSMContext):
    username = message.text
    data = await state.get_data()
    user = db_request.get_user(username=username)
    if user:
        db_request.update_user(id=user.id, updated_fields={'is_admin' : True})
        text, reply_markup = inline_kb_admin(db_request)
        try:
            await data['admin_message'].edit_text(text=text, reply_markup=reply_markup)
        except:
            await message.answer(text=text, reply_markup=reply_markup)
            await data['admin_message'].delete()
        await data['message'].delete()
    else:
        text, reply_markup = inline_kb_addadmin()
        await data['message'].edit_text(text=f'Пользователь "{username}" не найден.\n\n' + text, reply_markup=reply_markup)
    
    await message.delete()

@admin_messages_router.message(Form.addcoupon)
async def addcoupon(message: Message, db_request: DbRequests, state: FSMContext):
    data = await state.get_data()
    await message.delete()
    if not data['name']:
        if not db_request.get_coupon(name=message.text):
            await state.update_data(name=message.text)
            text, reply_markup = inline_kb_addcoupon(stage='sum')
            await data['message'].edit_text(text=text, reply_markup=reply_markup)
        else:
            text, reply_markup = inline_kb_addcoupon(stage='name')
            await data['message'].edit_text(text=f'Купон с названием "{message.text}" уже существует!\n\n' + text, reply_markup=reply_markup)
    else:
        try:
            sum = int(message.text)
            coupon = db_request.create_coupon(name=data['name'], sum=sum)
            text, reply_markup = inline_kb_admin_coupon(db_request, coupon_id=coupon.id)
            await data['admin_message'].edit_text(text=text, reply_markup=reply_markup)
            await state.clear()
        except:
            pass