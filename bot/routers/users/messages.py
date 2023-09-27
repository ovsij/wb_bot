from aiogram.types import Message
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.enums.parse_mode import ParseMode

from bot.database.database import *
from bot.database.functions.db_requests import DbRequests
from bot.keyboards import *
from bot.utils.states import *
from bot.wildberries import *

user_messages_router = Router()

@user_messages_router.message(Form.wb_token)
async def get_wb_token(message: Message, db_request: DbRequests, state: FSMContext):
    token = message.text
    data = await state.get_data()
    report = Statistics.get_reportDetailByPeriod(token)
    if report:
        brand_name = report['brand_name']
        
        if data['stage'] == 'connect':
            seller = db_request.create_seller(name=brand_name, user_id=db_request.get_user(tg_id=str(message.from_user.id)).id, token=token)
            text, reply_markup = inline_kb_sucсess_start(seller.id)
        elif data['stage'] == 'changeapifbo':
            seller = db_request.update_seller(id=data['seller_id'], name=brand_name, token=token, products=[])
            text, reply_markup = inline_kb_shop_settings(db_request, seller_id=seller.id, tg_id=str(message.from_user.id))
        elif data['stage'] == 'add_seller':
            seller = db_request.create_seller(name=brand_name, user_id=db_request.get_user(tg_id=str(message.from_user.id)).id, token=token)
            text, reply_markup = inline_kb_settings(db_request, tg_id=str(message.from_user.id))
        await state.clear()
        await message.answer(text=text, reply_markup=reply_markup)
    else:
        text, reply_markup = inline_kb_unsucсess_start()
        await message.answer(text=text, reply_markup=reply_markup)
    await message.delete()

@user_messages_router.message(Form.stockreserve)
async def get_stockreserve(message: Message, db_request: DbRequests, state: FSMContext):
    try:
        stock_reserve = int(message.text)
        
        if stock_reserve > 3 and stock_reserve < 60:
            data = await state.get_data()
            employee = db_request.get_employee(seller_id=data['seller_id'], user_id=db_request.get_user(tg_id=str(message.from_user.id)).id)
            db_request.update_employee(id=employee.id, stock_reserve=stock_reserve)
            text, reply_markup = inline_kb_stockreserve(db_request, seller_id=data['seller_id'], tg_id=str(message.from_user.id))
            await data['message'].edit_text(text=text, reply_markup=reply_markup)
        else:
            pass
    except:
        pass
    await message.delete()

@user_messages_router.message(Form.addusercoupon)
async def addusercoupon(message: Message, db_request: DbRequests, state: FSMContext):
    coupon = db_request.get_coupon(name=message.text)
    data = await state.get_data()
    if coupon:
        user = db_request.get_user(tg_id=str(message.from_user.id))
        if coupon.id in [c.id for c in db_request.get_coupon(user_id=user.id)]:
            text, reply_markup = inline_kb_coupon()
            await data['message'].edit_text(text=f'Вы уже использовали купон "{message.text}". \n\n' + text, reply_markup=reply_markup)
        else:
            user = db_request.update_user(tg_id=str(message.from_user.id), coupon_id=coupon.id)
            user, _ = db_request.create_transaction(user_id=user.id, sum=coupon.sum, type=True, coupon_name=message.text)
            text, reply_markup = inline_kb_coupon()
            await data['message'].edit_text(text=f'Вы применили купон "{message.text}". \n\nВаш баланс: {user.balance}₽', reply_markup=reply_markup)
    else:
        text, reply_markup = inline_kb_coupon()
        await data['message'].edit_text(text=f'Купон с названием "{message.text}" не найден...\n\n' + text, reply_markup=reply_markup)
    await message.delete()

@user_messages_router.message(Form.addnews)
async def addnews(message: Message, db_request: DbRequests, state: FSMContext):
    db_request.create_news(text=message.text)
    news_ids = [n.id for n in db_request.get_news()]
    text, reply_markup = inline_kb_news(db_request, news_id=news_ids[-1], tg_id=str(message.from_user.id))
    await message.answer(text=text, reply_markup=reply_markup)
    await message.delete()