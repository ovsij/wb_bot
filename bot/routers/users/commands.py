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

user_commands_router = Router()

@user_commands_router.message(Command(commands=["start", "my"]))
async def cmd_start(message: Message, db_request: DbRequests, state: FSMContext):
    print(message.text)
    user = db_request.get_user(tg_id=str(message.from_user.id))
    if db_request.user_seller_exists(user_id=user.id):
        # обработка добавления/удаления в избанное и добвления/удаления товаров в архив
        if 'favorites' in message.text:
            try:
                user = db_request.get_user(tg_id=str(message.from_user.id))
                product = db_request.get_product(id=int(message.text.split('_')[-1]))
                employee = db_request.get_employee(seller_id=product.seller.id, user_id=user.id)
                db_request.update_employee(id=employee.id, favorites=product.id)
                data = await state.get_data()
                text, reply_markup = inline_kb_stock_myproducts(db_request, tg_id=str(message.from_user.id), page=data['page'], filter=data['filter'])
                await data['msg_to_edit'].edit_text(text=text, reply_markup=reply_markup)
            except:
                pass
        elif 'archive' in message.text:
            try:
                user = db_request.get_user(tg_id=str(message.from_user.id))
                product = db_request.get_product(id=int(message.text.split('_')[-1]))
                employee = db_request.get_employee(seller_id=product.seller.id, user_id=user.id)
                db_request.update_employee(id=employee.id, archive=product.id)
                data = await state.get_data()
                text, reply_markup = inline_kb_stock_myproducts(db_request, tg_id=str(message.from_user.id), page=data['page'], filter=data['filter'])
                await data['msg_to_edit'].edit_text(text=text, reply_markup=reply_markup)
            except:
                pass
        # обработка обычного старта если сотрудник уже проходил по ссылке добавления сотрудника
        else:
            text, reply_markup = inline_kb_my(db_request, tg_id=str(message.from_user.id))
            await message.answer(text=text, reply_markup=reply_markup)
    else:
        if message.text in ['/start', '/my']:
            text, reply_markup = inline_kb_start()
            await message.answer(text=text, reply_markup=reply_markup)

        elif 'addemployee' in message.text:
                seller_id = int(message.text.strip('/start ').split('_')[2])
                db_request.update_seller(id=seller_id, user_id=user.id)
                await message.answer('✅ Поздравляем! Успешное подключение.\n🥷🏻 {bot name} работает на вас 🤜🏻')
                text, reply_markup = inline_kb_add_employee(db_request, seller_id=seller_id, tg_id=str(message.from_user.id))
                await message.answer(text=text, reply_markup=reply_markup)
        else:
            await message.answer('Сожалеем, но у вас нет доступа к этому действию...')
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

@user_commands_router.message(Command("stock"))
async def cmd_stock(message: Message, db_request: DbRequests):
    text, reply_markup = inline_kb_stocks(db_request, tg_id=str(message.from_user.id))
    await message.answer(text=text, reply_markup=reply_markup)
    await message.delete()    

@user_commands_router.message(Command("reports"))
async def cmd_reports(message: Message, db_request: DbRequests):
    text, reply_markup = inline_kb_reports(db_request, tg_id=str(message.from_user.id))
    await message.answer(text=text, reply_markup=reply_markup)

@user_commands_router.message(Command("search"))
async def cmd_search(message: Message, state: FSMContext):
    await state.set_state(Form.search_keywords)
    text = inline_kb_search_keywords()
    await message.answer(text=text, parse_mode='HTML')

@user_commands_router.message(Command("export"))
async def cmd_export(message: Message, db_request: DbRequests):
    text = inline_kb_export()
    await message.answer(text=text)

    text = as_line(f'ID: ', Code(str(message.from_user.id)))
    await message.answer(text=text.as_html())

    text, reply_markup = inline_kb_token(db_request, tg_id=str(message.from_user.id))
    await message.answer(text=text, reply_markup=reply_markup)

@user_commands_router.message(Command("create"))
async def cmd_create(message: Message, db_request: DbRequests):
    logging.info('Creating')
    user = db_request.get_user(tg_id=str(message.from_user.id))
    sellers_ids = [s.id for s in db_request.get_seller(user_id=user.id) if s.is_active]
    products = db_request.get_product(seller_id=sellers_ids)
  
    for p in products:
        start = datetime.now()
        print(f'start {p} - {start}')
        size = p.techSize if p.techSize != '0' else ''
        seller = db_request.get_seller(id=p.seller.id)
        stock = sum([pw.quantity for pw in db_request.get_product_warehouse(product_id=p.id)])
        orders = db_request.get_order(product_id=p.id, period=f"{(datetime.now() - timedelta(days=1000)).strftime('%d.%m.%Y')} - {datetime.now().strftime('%d.%m.%Y')}")
        orders_90 = len(db_request.get_order(product_id=p.id, period=f"{(datetime.now() - timedelta(days=90)).strftime('%d.%m.%Y')} - {datetime.now().strftime('%d.%m.%Y')}"))
        orders_30 = len(db_request.get_order(product_id=p.id, period=f"{(datetime.now() - timedelta(days=30)).strftime('%d.%m.%Y')} - {datetime.now().strftime('%d.%m.%Y')}"))
        orders_14 = len(db_request.get_order(product_id=p.id, period=f"{(datetime.now() - timedelta(days=14)).strftime('%d.%m.%Y')} - {datetime.now().strftime('%d.%m.%Y')}"))
        try:
            quantity_till = int(stock / (orders_90 / 90))
        except:
            quantity_till = 0
        employee = db_request.get_employee(user_id=user.id, seller_id=p.seller.id)
        orders_N = len(db_request.get_order(product_id=p.id, period=f"{(datetime.now() - timedelta(days=employee.stock_reserve)).strftime('%d.%m.%Y')} - {datetime.now().strftime('%d.%m.%Y')}"))
        forsupply_14 = 0 if orders_14 <= stock else int((orders_14 / 14) * 14 - stock)
        forsupply_N = 0 if orders_N <= stock else int((orders_N / 14) * 14 - stock)
        sales_90 = db_request.get_sale(product_id=p.id, period=f"{(datetime.now() - timedelta(days=90)).strftime('%d.%m.%Y')} - {datetime.now().strftime('%d.%m.%Y')}", type='S')
        print(sales_90)
        print('-----------')
        #buyout
        gnumbers = [s['gNumber'] for s in sales_90]
        
        orders_list = [o for o in orders if o['gNumber'] in gnumbers]
        try:
            buyout = int((len(sales_90) / len(orders_list)) * 100)
        except:
            buyout = 0
        abc, abc_percent = get_abc(db_request, product_id=p.id, seller_id=seller.id)
        result = [f'{p.nmId}_{size}', p.nmId, size, seller.name, p.supplierArticle, stock, quantity_till, orders_90, orders_30, orders_14, employee.stock_reserve, forsupply_14, forsupply_N, len(sales_90), buyout, p.rating, datetime.now().strftime('%d.%m.%Y %H:%M'), abc_percent, abc]
        db_request.create_exportmain(seller_id=seller.id,
                                     nmId_size=f'{p.nmId}_{size}',
                                     nmId=p.nmId,
                                     size=size,
                                     seller_name=seller.name,
                                     product_name=p.supplierArticle,
                                     quantity=stock,
                                     quantity_till=quantity_till,
                                     orders_90=orders_90,
                                     orders_30=orders_30,
                                     orders_14=orders_14,
                                     stock_reserve=employee.stock_reserve,
                                     forsupply_14=forsupply_14,
                                     forsupply_N=forsupply_N,
                                     sales_90=len(sales_90),
                                     buyout=buyout,
                                     rating=p.rating,
                                     updatet_at=datetime.now(),
                                     abc_percent=abc_percent,
                                     abc=abc)