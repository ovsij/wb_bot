import asyncio, aiohttp
from aiogram.types import Message, FSInputFile
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.enums.parse_mode import ParseMode
from datetime import datetime
import re

from bot.database.database import *
from bot.database.functions.db_requests import DbRequests
from bot.keyboards import *
from bot.utils.states import *
from bot.utils.telegraph import *
from bot.wildberries import *

user_messages_router = Router()

@user_messages_router.message(Form.wb_token)
async def get_wb_token(message: Message, db_request: DbRequests, state: FSMContext):
    token = message.text
    data = await state.get_data()
    report = await Statistics.get_reportDetailByPeriod(token)
    if report:
        seller_name = await WbParser.get_seller_name(article=report[0]['nm_id'])
        seller_name = seller_name.replace('Индивидуальный предприниматель', 'ИП')
        if data['stage'] == 'connect' or data['stage'] == 'add_seller':
            seller = db_request.create_seller(name=seller_name, user_id=db_request.get_user(tg_id=str(message.from_user.id)).id, token=token)
            if data['stage'] == 'connect':
                text, reply_markup = inline_kb_sucсess_start(seller.id)
            elif data['stage'] == 'add_seller':
                text, reply_markup = inline_kb_settings(db_request, tg_id=str(message.from_user.id))
            if not db_request.get_seller(id=seller.id).activation_date:
                if await Statistics.check_orders(db_request, seller):
                    # если в течение последних 100 дней были заказы активируем продавца
                    db_request.update_seller(id=seller.id, is_active=True, activation_date=datetime.now(), test_period=True)
                    asyncio.create_task(update_seller(seller, tariff=True))

        elif data['stage'] == 'changeapifbo':
            seller = db_request.update_seller(id=data['seller_id'], name=seller_name, token=token, products=[])
            text, reply_markup = inline_kb_shop_settings(db_request, seller_id=seller.id, tg_id=str(message.from_user.id))
        
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

            sellers = db_request.get_seller(user_id=user.id)
            for seller in sellers:
                if not seller.is_active:
                    DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
                    paymet_sum = round(seller.tariff / DAYS[datetime.now().month - 1], 2)
                    db_request.create_transaction(user_id=user.id, sum=paymet_sum, type=False)
                    db_request.update_seller(id=seller.id, is_active=True, last_payment_date=datetime.now())

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

@user_messages_router.message(Form.reports_timedelta)
async def reports_timedelta(message: Message, db_request: DbRequests, state: FSMContext):
    date = message.text
    if re.fullmatch('\d*.\d*.\d*', date) or re.fullmatch('\d*.\d*.\d* - \d*.\d*.\d*', date):
        data = await state.get_data()
        text, reply_markup = await inline_kb_reports_byperiod(db_request, state, tg_id=str(message.from_user.id), period=date, page=1)
        await message.delete()
        await data['msg_for_delete'].delete()
        await data['msg_for_edit'].edit_text(text=text, reply_markup=reply_markup)
    else:
        await message.delete()

@user_messages_router.message(Form.search)
async def reports_search(message: Message, db_request: DbRequests, state: FSMContext):
    if len(message.text) > 100:
        pass
    else:
        data = await state.get_data()
        await data['msg_to_delete'].delete()
        await message.delete()
        if data['type'] == 'myproducts' or data['type'] == 'favorites' or data['type'] == 'archive':
            text, reply_markup = inline_kb_stock_myproducts(db_request, tg_id=str(message.from_user.id), page=1, filter=data['type'], search=message.text)
        elif data['type'] == 'orders':
            text, reply_markup = inline_kb_orders(db_request, tg_id=str(message.from_user.id), page=1, search=message.text)
        elif data['type'] == 'sales':
            text, reply_markup = inline_kb_sales(db_request, tg_id=str(message.from_user.id), page=1, search=message.text)
        elif data['type'] == 'report':
            text, reply_markup = inline_kb_reports_byperiod(db_request, state, tg_id=str(message.from_user.id), period=data['period'], page=1, search=message.text)
        await data['msg_to_edit'].edit_text(text=text, reply_markup=reply_markup)
        await state.update_data(search=message.text)

@user_messages_router.message(Form.search_keywords)
async def reports_search_keywords(message: Message, db_request: DbRequests, state: FSMContext):
    article = ''
    if '.ru' in message.text:
        article = re.search('\d\d\d\d\d+', message.text)
        article = article.group()
    else:
        try:
            int(message.text)
            article = message.text
        except:
            pass
    print('art')
    print(article)
    if len(article) > 0:
        url = f'https://wbconcierge.onrender.com/search/{article}'
        text, reply_markup = inline_kb_searchresult(url)
        await message.answer(text=text, reply_markup=reply_markup)
                    
