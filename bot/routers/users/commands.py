import asyncio

from aiogram.types import Message
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.enums.parse_mode import ParseMode

from bot.database.database import *
from bot.database.functions.db_requests import DbRequests
from bot.keyboards import *
from bot.wildberries import *
from bot.utils.states import *

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
async def cmd_stocks(message: Message, db_request: DbRequests):
    text, reply_markup = inline_kb_stocks(db_request, tg_id=str(message.from_user.id))
    await message.answer(text=text, reply_markup=reply_markup)
    await message.delete()    

@user_commands_router.message(Command("reports"))
async def cmd_stocks(message: Message, db_request: DbRequests):
    text, reply_markup = inline_kb_reports(db_request, tg_id=str(message.from_user.id))
    await message.answer(text=text, reply_markup=reply_markup)

@user_commands_router.message(Command("search"))
async def cmd_stocks(message: Message, state: FSMContext):
    await state.set_state(Form.search_keywords)
    text = inline_kb_search_keywords()
    await message.answer(text=text, parse_mode='HTML')


import aiohttp
from tqdm import tqdm
import concurrent.futures
import requests
@user_commands_router.message(Command("create"))
async def cmd_stocks(message: Message, state: FSMContext, db_request: DbRequests):
    print('create keywords')
    db_request.create_keywords()
    print('finish create keywords')

@user_commands_router.message(Command("go"))
async def cmd_stocks(message: Message, state: FSMContext, db_request: DbRequests):
    print('start')
    keywords = db_request.get_keywords()
    print('keywords extracted from db')
    
    start = datetime.now()
    #async with aiohttp.ClientSession(trust_env=True) as session:
    session = aiohttp.ClientSession(trust_env=True)
    r_session = requests.Session()

    tasks = set()
    #for keyword in keywords[:10000]:

    CONNECTIONS = 100

    with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
        future_to_url = [executor.submit(get_request_classic, keyword) for keyword in keywords[:100000]]
        for future in tqdm(concurrent.futures.as_completed(future_to_url), total=len(keywords[:100000])):
            #try:
            data = future.result() 
            db_request.update_keyword(id=data['keyword'], search=data['search'], total=data['total'])
            #except Exception as exc:   
            #    print(exc) 
                
    
            
        #await get_request(db_request, keyword, start, session)
        #tasks.add(asyncio.create_task(get_request(db_request, keyword, start, session)))
    #await asyncio.gather(*tasks)
    #print('tasks created')
    #await session.close()
    end = datetime.now()
    print(f'Time {end-start}')
            

async def get_request(db_request, keyword, start, session):
    
    url = 'https://search.wb.ru/exactmatch/ru/common/v4/search'
    params_first = {'TestGroup': 'control', 'TestID':351, 'appType':1, 'curr': 'rub', 'dest': -1257786, 'filters': 'xsubject', 'query':keyword[1], 'resultset': 'filters'}
    async with session.get(url, params=params_first, ssl=False) as response:
        result = await response.json(content_type='text/plain')
        total = result['data']['total']
        print(total)
    print(keyword)
    products = []
    for page in range(1, 4):
        params_second = {'TestGroup': 'control', 'TestID':351, 'appType':1, 'curr': 'rub', 'dest': -1257786, 'page': page, 'query':str(keyword[1]), 'resultset': 'catalog', 'sort':'popular', 'suppressSpellcheck': 'false'}
        async with session.get(url, params=params_second, ssl=False) as response:
            if response.status == 200:
                try:
                    result = await response.json(content_type='text/plain')
                    page_products = [p['id'] for p in result['data']['products']]
                    products.append({page: page_products})
                    print(page)
                except:
                    print('НЕ ПРОШЕЛ ЗАПРОС!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            else:
                print('НЕ ПРОШЕЛ ЗАПРОС!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    print(products)
    db_request.update_keyword(id=keyword[0], search=products, total=total)


def get_request_classic(keyword):
    
    url = 'https://search.wb.ru/exactmatch/ru/common/v4/search'
    params_first = {'TestGroup': 'control', 'TestID':351, 'appType':1, 'curr': 'rub', 'dest': -1257786, 'filters': 'xsubject', 'query':keyword[1], 'resultset': 'filters'}
    response = requests.get(url, params=params_first)
    result = response.json()
    total = result['data']['total']
    #print(keyword)
    #print(total)
    
    products = []
    for page in range(1, 4):
        params_second = {'TestGroup': 'control', 'TestID':351, 'appType':1, 'curr': 'rub', 'dest': -1257786, 'page': page, 'query':str(keyword[1]), 'resultset': 'catalog', 'sort':'popular', 'suppressSpellcheck': 'false'}
        response = requests.get(url, params=params_second)
        if response.status_code == 200:
            try:
                result = response.json()
                page_products = [p['id'] for p in result['data']['products']]
                products.append({page: page_products})
                #print(page)
            except:
                print('НЕ ПРОШЕЛ ЗАПРОС!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        else:
            print('НЕ ПРОШЕЛ ЗАПРОС!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    #print(products)
    return {'keyword': keyword[0], 'search': products, 'total': total}
    