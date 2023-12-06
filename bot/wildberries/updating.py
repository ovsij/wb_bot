import asyncio
from aiogram.types import FSInputFile
from aiogram.utils.formatting import *
from datetime import date, datetime, timedelta
import logging
import pandas as pd

from bot.database.functions.db_requests import DbRequests
from bot import bot
from bot.keyboards import *
from bot.wildberries import *
from bot.utils import abc_analysis
from bot.utils.utils import get_difference, get_warehouse_quantity



LOGISTICS = {
    'Астана': 7,
    'Атакент': 7,
    'Санкт-Петербург': 24.5,
    'Санкт-Петербург Шушары': 24.5,
    'Невинномысск': 24.5,
    'Краснодар': 33.25,
    'СЦ Кузнецк': 32,
    'Краснодар 2': 32,
    'Тула': 36.75,
    'Пушкино': 36.75,
    'Радумля 1': 36.75,
    'Радумля СГТ': 36.75,
    'Казань': 52.5,
    'Санкт-Петербург 2': 44,
    'Санкт-Петербург Уткина Заводь': 42,
    'Вёшки': 42,
    'Белая дача': 45.5,
    'МЛП-Подольск': 48,
    'Электросталь': 56,
    'Белые Столбы': 56,
    'Коледино': 54.25,
    'Подольск': 56,
    'Хабаровск': 56,
    'Чехов 2': 50.75,
    'Маркетплейс': 52.5,
    'Екатеринбург': 105,
    'Екатеринбург - Перспективный 12': 105,
    'Екатеринбург 2': 134,
    'Екатеринбург - Испытателей 14г': 122.5,
    'Новосибирск': 119,
}

async def inline_kb_new_order_addit(db_request, order_id : int, minus_total : int):
    order = db_request.get_order(id=order_id)
    product = db_request.get_product(id=order.product.id)
    today_orders = [o['totalPrice'] * (1 - o['discountPercent'] / 100) for o in db_request.get_order(seller_id=product.seller.id, select_for='reports', period='today')]
    price = round(order.totalPrice * (1 - order.discountPercent / 100), 2)
    sales_list = db_request.get_sale(product_id=product.id, type='S', period=f"{(datetime.now() - timedelta(days=91)).strftime('%d.%m.%Y')} - {datetime.now().strftime('%d.%m.%Y')}")
    try:
        spp = [s['spp'] for s in sales_list if s['nmId'] == order.nmId][-1]
    except:
        spp = 0
    comission = db_request.get_comission(subject=order.subject)
    try:
        logistic_price = f": {LOGISTICS[order.warehouseName]}₽"
    except:
        logistic_price = ''
    text = as_line(order.date,
                   f'🛒 Заказ [{len(today_orders) - minus_total}]: {price}₽',
                   f'🛍️ WB скидка: {int(price * (spp / 100))}₽ ({spp}%)',
                   f'💼 Комиссия базовая: {round(price * (1 - comission/100), 2)}₽ ({comission}%)',
                   f'🌐 {order.warehouseName} → {order.oblast}{logistic_price}',
                   '',
                   sep='\n')
    return text.as_html()
    


async def inline_kb_new_order(db_request, order_id : int, employee : int, minus_total : int, search=None):
    seller = db_request.get_seller(id=employee.seller.id)
    order = db_request.get_order(id=order_id)
    product = db_request.get_product(id=order.product.id)
    price = round(order.totalPrice * (1 - order.discountPercent / 100), 2)
    product_warehouse = db_request.get_product_warehouse(product_id=product.id)
    sales_list = db_request.get_sale(product_id=product.id, type='S', period=f"{(datetime.now() - timedelta(days=91)).strftime('%d.%m.%Y')} - {datetime.now().strftime('%d.%m.%Y')}")
    try:
        spp = [s['spp'] for s in sales_list if s['nmId'] == order.nmId][-1]
    except:
        spp = 0
    inWayToClient = sum([p.inWayToClient for p in product_warehouse])
    inWayFromClient = sum([p.inWayFromClient for p in product_warehouse])
    sales = len(sales_list)
    gNumbers = [s['gNumber'] for s in sales_list]
    orders_90 = db_request.get_order(product_id=product.id, period=f"{(datetime.now() - timedelta(days=90)).strftime('%d.%m.%Y')} - {datetime.now().strftime('%d.%m.%Y')}")
    orders_76 = db_request.get_order(product_id=product.id, period=f"{(datetime.now() - timedelta(days=76)).strftime('%d.%m.%Y')} - {datetime.now().strftime('%d.%m.%Y')}")
    today_orders = [o['totalPrice'] * (1 - o['discountPercent'] / 100) for o in db_request.get_order(seller_id=product.seller.id, select_for='reports', period='today')]
    print(today_orders)
    today_orders_such = [o['totalPrice'] * (1 - o['discountPercent'] / 100) for o in orders_76 if o['date'].date() == datetime.now().date()]
    yesterday_orders_such = [o['totalPrice'] * (1 - o['discountPercent'] / 100) for o in orders_76 if o['date'].date() == (datetime.now() - timedelta(days=1)).date() and o['nmId'] == order.nmId]
    #orders_list = [o for o in orders if o['gNumber'] in gNumbers]
    #saled_orders = [s['order'] for s in sales_list]
    try:
        buyout = int((sales/len(orders_76)) * 100)
    except:
        buyout = 0
    abc, abc_percent = abc_analysis.get_abc(db_request, product_id=product.id, seller_id=product.seller.id)
    abc_emoji = '🟩' if abc == 'A' else '🟧' if abc == 'B' else '🟥'
    
    warehouses, quantity_till_total, quantity_total = get_warehouse_quantity(db_request, orders_90, product_warehouse)

    try:
        logistic_price = f": {LOGISTICS[order.warehouseName]}₽"
        
    except:
        logistic_price = ''

    comission = db_request.get_comission(subject=product.subject)
    
    text = as_line(order.date,
                   seller.name,
                   '',
                   f'🛒 Заказ [{len(today_orders) - minus_total}]: {price}₽',
                   f'📈 Сегодня: {len(today_orders)} на {int(sum(today_orders))}₽',
                   f'🆔 Арт: {order.nmId} ',
                   f'🛍️ WB скидка: {int(price * (spp / 100))}₽ ({spp}%)',
                   f'📁 {product.subject}',
                   f'🏷 {product.brand} / {product.supplierArticle}',
                   f'⭐ Рейтинг: {product.rating}',
                   f'💬 Отзывы: {product.reviews}',
                   f'💵 Сегодня таких: {len(today_orders_such)} на {int(sum(today_orders_such))}₽',
                   f'💶 Вчера таких: {len(yesterday_orders_such)} на {int(sum(yesterday_orders_such))}₽',
                   f'{abc_emoji} ABC-анализ: {abc} ({abc_percent}%)',
                   f'💼 Комиссия базовая: {round(price * (comission/100), 2)}₽ ({comission}%)',
                   f'💎 Выкуп за 3 мес: {buyout}% ({sales}/{len(orders_76)})',
                   f'🌐 {order.warehouseName} → {order.oblast}{logistic_price}',
                   f'🚛 В пути до клиента: {inWayToClient}',
                   f'🚚 В пути возвраты: {inWayFromClient}',
                   '',
                   sep='\n'
                   )
    for name, quantity in warehouses.items():
        try:
            text += as_line(f'📦 {name}: {quantity[0]} шт. хватит на {quantity[1]} дн.')
        except:
            ...

    if len(warehouses) > 1 and employee.stock_reserve < quantity_till_total:
        text += as_line(f'📦 Всего: {quantity_total} шт. хватит на {quantity_till_total} дн.')
    elif len(warehouses) > 1 and employee.stock_reserve > quantity_till_total:
        text += as_line(f'📦 Всего: {quantity_total} шт. хватит на ⚠️ {quantity_till_total} дн.')
    
    if employee.stock_reserve > quantity_till_total:
            income = int((len(orders_90)/90) * employee.stock_reserve - quantity_total)
            text += as_line(f'🚗 Пополните склад на {income} шт.')
    
    
    if employee.is_key_words and search:
        #print(order.nmId)
        keywords = db_request.get_keywords(article=order.nmId, is_today=True)
        #print(keywords)
        #print(len(keywords))
        text += as_line('\n🔍 Позиции в поиске:\n')
        data = []
        for keyword in keywords:
            page = 1 if int(order.nmId) in keyword.search_1 else 2 if int(order.nmId) in keyword.search_2 else 3
            index = keyword.search_1.index(int(order.nmId)) + 1 if page == 1 else keyword.search_2.index(int(order.nmId)) + 1 if page == 2 else keyword.search_3.index(int(order.nmId)) + 1
            data.append([keyword.keyword, page, index, keyword.requests, keyword.total])
        df = pd.DataFrame(data=data, columns=['keyword', 'page', 'index', 'requests', 'total'])
        df_sort = df.sort_values(['page', 'index', 'requests'], ascending=[True, True, True])
        len_range = 7 if len(df_sort) > 6 else len(df_sort)
        for i in range(1, len_range):
            today_keyword = db_request.get_keyword(keyword=df_sort.iloc[i]['keyword'], is_today=True)
            yesterday_keyword = db_request.get_keyword(keyword=df_sort.iloc[i]['keyword'], is_today=False)
            if yesterday_keyword:
                try:
                    difference = get_difference(article=int(order.nmId), today=today_keyword, yesterday=yesterday_keyword)
                except:
                    difference = ''
            else:
                difference = ''
            text += as_line(df_sort.iloc[i]['keyword'],
                            as_line(TextLink(f"{df_sort.iloc[i]['page']}-{df_sort.iloc[i]['index']}", url=f"https://www.wildberries.ru/catalog/0/search.aspx?sort=popular&search={df_sort.iloc[i]['keyword'].replace(' ', '+')}"), difference),
                            sep='\n')
            
    url = f'https://wbconcierge.onrender.com/search/{order.nmId}'
    text_and_data = [
        ['Позиции в поиске 🔍', url]
    ]
    reply_markup = InlineConstructor.create_kb(text_and_data=text_and_data, button_type=['web_app'])

    ###
    is_all = all([employee.order_notif_end, employee.order_notif_ending, employee.order_notif_commission, employee.order_notif_favorites])
    if is_all:
        return text.as_html(), reply_markup
    else:
        if employee.order_notif_end and quantity_total == 0 \
            or employee.order_notif_ending and employee.stock_reserve > quantity_till_total \
            or employee.order_notif_favorites and product in employee.favorites:

            return text.as_html(), reply_markup
        else:
            return False, False
        
async def inline_kb_new_sale_addit(db_request, sale_id : int, minus_total : int):
    sale = db_request.get_sale(id=sale_id)
    product = db_request.get_product(id=sale.product.id)
    today_sales = [s for s in db_request.get_sale(seller_id=product.seller.id, select_for='reports', period='today', type=str(sale.saleID)[0])]
    price = sale.priceWithDisc
    spp = sale.spp
    comission = db_request.get_comission(subject=sale.subject)
    try:
        logistic_price = f": {LOGISTICS[sale.warehouseName]}₽"
    except:
        logistic_price = ''
    text = as_line(sale.date,
                   f'🛒 Заказ [{len(today_sales) - minus_total}]: {price}₽',
                   f'🛍️ WB скидка: {int(price * (spp / 100))}₽ ({spp}%)',
                   f'💼 Комиссия базовая: {round(price * (1 - comission/100), 2)}₽ ({comission}%)',
                   f'🌐 {sale.warehouseName} → {sale.regionName}{logistic_price}',
                   '',
                   sep='\n')
    return text.as_html()

async def inline_kb_new_sale(db_request, sale_id : int, employee : int, minus_total : int, search : bool = None):
    seller = db_request.get_seller(id=employee.seller.id)
    sale = db_request.get_sale(id=sale_id)
    sales_order = db_request.get_order(odid=sale.odid)
    try:
        date_from_order = (sale.date - sales_order.date).days
    except:
        date_from_order = ''
    product = db_request.get_product(id=sale.product.id)
    price = sale.priceWithDisc
    product_warehouse = db_request.get_product_warehouse(product_id=product.id)
    sales_list = db_request.get_sale(product_id=product.id, type='S', period=f"{(datetime.now() - timedelta(days=91)).strftime('%d.%m.%Y')} - {datetime.now().strftime('%d.%m.%Y')}")
    spp = sale.spp
    inWayToClient = sum([p.inWayToClient for p in product_warehouse])
    inWayFromClient = sum([p.inWayFromClient for p in product_warehouse])
    sales = len(sales_list) - inWayFromClient
    gNumbers = [s['gNumber'] for s in sales_list]
    orders_90 = db_request.get_order(product_id=product.id, period=f"{(datetime.now() - timedelta(days=90)).strftime('%d.%m.%Y')} - {datetime.now().strftime('%d.%m.%Y')}")
    orders_76 = db_request.get_order(product_id=product.id, period=f"{(datetime.now() - timedelta(days=76)).strftime('%d.%m.%Y')} - {datetime.now().strftime('%d.%m.%Y')}")
    
    today_sales = [s['priceWithDisc'] for s in db_request.get_sale(seller_id=product.seller.id, select_for='reports', period='today', type=str(sale.saleID)[0])]
    today_sales_such = [s['priceWithDisc'] for s in sales_list if s['date'].date() == datetime.now().date()]
    yesterday_sales_such = [s['priceWithDisc'] for s in sales_list if s['date'].date() == (datetime.now() - timedelta(days=1)).date()]
    #orders_list = [o for o in orders if o['gNumber'] in gNumbers]
    buyout = int((sales/len(orders_76)) * 100)
    abc, abc_percent = abc_analysis.get_abc(db_request, product_id=product.id, seller_id=product.seller.id)
    abc_emoji = '🟩' if abc == 'A' else '🟧' if abc == 'B' else '🟥'
    warehouses, quantity_till_total, quantity_total = get_warehouse_quantity(db_request, orders_90, product_warehouse)

    try:
        logistic_price = f": {LOGISTICS[sale.warehouseName]}₽"
        
    except:
        logistic_price = ''

    comission = db_request.get_comission(subject=product.subject)

    sale_type = '✅ Выкуп' if sale.saleID.startswith('S') else '⛔️ Отмена'
    text = as_line(sale.date,
                   seller.name,
                   '',
                   f'{sale_type} [{len(today_sales) - minus_total}]: {price}₽',
                   f'⏱️ От даты заказа: {date_from_order} дн.',
                   f'📈 Сегодня: {len(today_sales)} на {int(sum(today_sales))}₽',
                   f'🆔 Арт: {sale.nmId} ',
                   f'🛍️ WB скидка: {int(price * (spp / 100))}₽ ({spp}%)',
                   f'📁 {product.subject}',
                   f'🏷 {product.brand} / {product.supplierArticle}',
                   f'⭐ Рейтинг: {product.rating}',
                   f'💬 Отзывы: {product.reviews}',
                   f'💵 Сегодня таких: {len(today_sales_such)} на {int(sum(today_sales_such))}₽',
                   f'💶 Вчера таких: {len(yesterday_sales_such)} на {int(sum(yesterday_sales_such))}₽',
                   f'{abc_emoji} ABC-анализ: {abc} ({abc_percent}%)',
                   f'💼 Комиссия базовая: {round(price * (1 - comission/100), 2)}₽ ({comission}%)',
                   f'💎 Выкуп за 3 мес: {buyout}% ({sales}/{len(orders_76)})',
                   f'🌐 {sale.warehouseName} → {sale.regionName}{logistic_price}',
                   f'🚛 В пути до клиента: {inWayToClient}',
                   f'🚚 В пути возвраты: {inWayFromClient}',
                   '',
                   sep='\n'
                   )
    

    for name, quantity in warehouses.items():
        try:
            text += as_line(f'📦 {name}: {quantity[0]} шт. хватит на {quantity[1]} дн.')
        except:
            ...

    if len(warehouses) > 1 and employee.stock_reserve < quantity_till_total:
        text += as_line(f'📦 Всего: {quantity_total} шт. хватит на {quantity_till_total} дн.')
    elif len(warehouses) > 1 and employee.stock_reserve > quantity_till_total:
        text += as_line(f'📦 Всего: {quantity_total} шт. хватит на ⚠️ {quantity_till_total} дн.')
    
    if employee.stock_reserve > quantity_till_total:
            income = int((len(orders_90)/90) * employee.stock_reserve - quantity_total)
            text += as_line(f'🚗 Пополните склад на {income} шт.')
    
    if employee.is_key_words and search:
        #print(order.nmId)
        keywords = db_request.get_keywords(article=sale.nmId, is_today=True)
        #print(keywords)
        #print(len(keywords))
        text += as_line('\n🔍 Позиции в поиске:\n')
        data = []
        for keyword in keywords:
            page = 1 if int(sale.nmId) in keyword.search_1 else 2 if int(sale.nmId) in keyword.search_2 else 3
            index = keyword.search_1.index(int(sale.nmId)) + 1 if page == 1 else keyword.search_2.index(int(sale.nmId)) + 1 if page == 2 else keyword.search_3.index(int(sale.nmId)) + 1
            data.append([keyword.keyword, page, index, keyword.requests, keyword.total])
        df = pd.DataFrame(data=data, columns=['keyword', 'page', 'index', 'requests', 'total'])
        df_sort = df.sort_values(['page', 'index', 'requests'], ascending=[True, True, True])
        len_range = 7 if len(df_sort) > 6 else len(df_sort)
        for i in range(1, len_range):
            today_keyword = db_request.get_keyword(keyword=df_sort.iloc[i]['keyword'], is_today=True)
            yesterday_keyword = db_request.get_keyword(keyword=df_sort.iloc[i]['keyword'], is_today=False)
            if yesterday_keyword:
                difference = get_difference(article=int(sale.nmId), today=today_keyword, yesterday=yesterday_keyword)
            else:
                difference = ''
            text += as_line(df_sort.iloc[i]['keyword'],
                            as_line(TextLink(f"{df_sort.iloc[i]['page']}-{df_sort.iloc[i]['index']}", url=f"https://www.wildberries.ru/catalog/0/search.aspx?sort=popular&search={df_sort.iloc[i]['keyword'].replace(' ', '+')}"), difference),
                            sep='\n')
            
    url = f'https://wbconcierge.onrender.com/search/{sale.nmId}'
    text_and_data = [
        ['Позиции в поиске 🔍', url]
    ]
    reply_markup = InlineConstructor.create_kb(text_and_data=text_and_data, button_type=['web_app'])

    ###
    is_all = all([employee.buyout_notif_end, employee.buyout_notif_ending, employee.buyout_notif_favorites])
    if is_all:
        return text.as_html(), reply_markup
    else:
        if employee.buyout_notif_end and quantity_total == 0 \
            or employee.buyout_notif_ending and employee.stock_reserve > quantity_till_total \
            or employee.buyout_notif_favorites and product in employee.favorites:
            
            return text.as_html(), reply_markup
        else:
            return False, False
        
async def inline_kb_add_order(db_request, order_id, minus_total):
    order = db_request.get_order(id=order_id)
    product = db_request.get_product(id=order.product.id)
    today_orders = [o['totalPrice'] * (1 - o['discountPercent'] / 100) for o in db_request.get_order(seller_id=product.seller.id, select_for='reports', period='today')]
    price = round(order.totalPrice * (1 - order.discountPercent / 100), 2)
    sales_list = db_request.get_sale(product_id=product.id, type='S', period=f"{(datetime.now() - timedelta(days=91)).strftime('%d.%m.%Y')} - {datetime.now().strftime('%d.%m.%Y')}")
    try:
        logistic_price = f": {LOGISTICS[order.warehouseName]}₽"
    except:
        logistic_price = ''
    text = as_line('', 
                   order.date,
                   f'🛒 Заказ [{len(today_orders) - minus_total}]: {price}₽',
                   f'💼 Комиссия базовая: {round(price * (1 - 19/100), 2)}₽ (19%)',
                   f'🌐 {order.warehouseName} → {order.oblast}{logistic_price}',
                   sep='\n')
    return text.as_html()
        


async def update_stocks(db_request, seller):
    logging.info(f'{seller.name}[{seller.id}] started stocks. Time: {datetime.now()}')
    """UPDATING STOCKS"""
    stocks = await Statistics.get_stocks(token=seller.token)
    for product in stocks:
        #await Statistics.get_nomenclature(db_request, seller, product['supplierArticle'])
        rating, reviews = await WbParser.get_rating(article=product['nmId'])
        await WbParser.get_image(article=product['nmId'])
        await db_request.create_product(seller_id=seller.id,
                                supplierArticle=product['supplierArticle'],
                                nmId=product['nmId'],
                                barcode=product['barcode'],
                                category=product['category'],
                                subject=product['subject'],
                                brand=product['brand'],
                                techSize=product['techSize'],
                                price=product['Price'],
                                discount=product['Discount'],
                                isSupply=product['isSupply'],
                                isRealization=product['isRealization'],
                                SCCode=product['SCCode'],
                                warehouseName=product['warehouseName'],
                                quantity=product['quantity'],
                                inWayToClient=product['inWayToClient'],
                                inWayFromClient=product['inWayFromClient'],
                                quantityFull=product['quantityFull'],
                                rating=rating,
                                reviews=reviews)

async def update_orders(db_request, seller, sending):
    orders = await Statistics.get_orders(db_request, seller)
    new_orders = {}
    if orders:
        logging.info(f'{seller.name}[{seller.id}] got {len(orders)} orders. Time: {datetime.now()}')
        for order in orders:
            print(order)
            new_order = db_request.create_order(seller_id=seller.id,
                                    gNumber=order['gNumber'],
                                    date=order['date'],
                                    lastChangeDate=order['lastChangeDate'],
                                    supplierArticle=order['supplierArticle'],
                                    techSize=order['techSize'],
                                    barcode=order['barcode'],
                                    totalPrice=order['totalPrice'],
                                    discountPercent=order['discountPercent'],
                                    warehouseName=order['warehouseName'],
                                    oblast=order['regionName'],
                                    incomeID=order['incomeID'],
                                    #odid=order['odid'],
                                    nmId=order['nmId'],
                                    subject=order['subject'],
                                    category=order['category'],
                                    brand=order['brand'],
                                    isCancel=order['isCancel'],
                                    cancel_dt=order['cancelDate'],
                                    sticker=order['sticker'],
                                    srid=order['srid'],
                                    orderType=order['orderType'],)
            if new_order != None:
                try:
                    new_orders[order['nmId']] += [new_order]
                except:
                    new_orders[order['nmId']] = [new_order]
        if not sending:
            return
        total_new_orders = len(new_orders)
        for employee in db_request.get_employee(seller_id=seller.id):
            if any([employee.order_notif_end, employee.order_notif_ending, employee.order_notif_commission, employee.order_notif_favorites]):
                for _, new_order_lst in new_orders.items():
                    text = None
                    if len(new_order_lst) == 1:
                        total_new_orders -= 1
                        text, reply_markup = await inline_kb_new_order(db_request, order_id=new_order_lst[0].id, employee=employee, minus_total=total_new_orders, search=True)
                    elif 4 > len(new_order_lst) > 1:
                        total_new_orders -= 1
                        text, reply_markup = await inline_kb_new_order(db_request, order_id=new_order_lst[0].id, employee=employee, minus_total=total_new_orders)
                        text += '\n➕ в том числе 👇🏻\n\n'
                        for addit_order in new_order_lst[1:]:
                            total_new_orders -= 1
                            text += await inline_kb_new_order_addit(db_request, order_id=addit_order.id, minus_total=total_new_orders)
                    else:
                        if len(new_order_lst) % 3 == 0:
                            range_num = int(len(new_order_lst) / 3)
                        else:
                            range_num = int(len(new_order_lst) / 3) + 1

                        for i in range(range_num):
                            total_new_orders -= 1
                            search = None if len(new_order_lst[i*3+1 : i*3+3]) > 0 else True
                            text, reply_markup = await inline_kb_new_order(db_request, order_id=new_order_lst[i*3].id, employee=employee, minus_total=total_new_orders, search=search)
                            
                            if text:
                                if not search:
                                    text += '\n➕ в том числе 👇🏻\n\n'
                                    for addit_order in new_order_lst[i*3+1 : i*3+3]:
                                        total_new_orders -= 1
                                        text += await inline_kb_new_order_addit(db_request, order_id=addit_order.id, minus_total=total_new_orders)
                                user = db_request.get_user(id=employee.user.id)
                                try:
                                    photo = FSInputFile(f'bot/database/images/{addit_order.nmId}.jpg', 'rb')
                                    await bot.send_photo(user.tg_id, photo=photo, caption=text, reply_markup=reply_markup)
                                except Exception as ex:
                                    logging.warning(ex)
                        return
                    if text:
                        user = db_request.get_user(id=employee.user.id)
                        try:
                            photo = FSInputFile(f'bot/database/images/{new_order_lst[0].nmId}.jpg', 'rb')
                            await bot.send_photo(user.tg_id, photo=photo, caption=text, reply_markup=reply_markup)
                        except Exception as ex:
                            logging.warning(ex)


async def update_sales(db_request, seller, sending):
    sales = await Statistics.get_sales(db_request, seller)
    if sales:
        logging.info(f'{seller.name}[{seller.id}] got {len(sales)} sales. Time: {datetime.now()}')
        new_sales = {}
        for sale in sales:
            new_sale = db_request.create_sale(seller_id=seller.id,
                                gNumber=sale['gNumber'],
                                date=sale['date'],
                                lastChangeDate=sale['lastChangeDate'],
                                supplierArticle=sale['supplierArticle'],
                                techSize=sale['techSize'],
                                barcode=sale['barcode'],
                                totalPrice=sale['totalPrice'],
                                discountPercent=sale['discountPercent'], 
                                isSupply=sale['isSupply'],
                                isRealization=sale['isRealization'],
                                warehouseName=sale['warehouseName'], 
                                countryName=sale['countryName'], 
                                oblastOkrugName=sale['oblastOkrugName'], 
                                regionName=sale['regionName'], 
                                incomeID=sale['incomeID'], 
                                saleID=sale['saleID'], 
                                #odid=sale['odid'], 
                                spp=sale['spp'], 
                                forPay=sale['forPay'], 
                                finishedPrice=sale['finishedPrice'], 
                                priceWithDisc=sale['priceWithDisc'], 
                                nmId=sale['nmId'], 
                                subject=sale['subject'], 
                                category=sale['category'], 
                                brand=sale['brand'], 
                                sticker=sale['sticker'], 
                                srid=sale['srid'], )
            if new_sale != None:
                try:
                    new_sales[sale['nmId']] += [new_sale]
                except:
                    new_sales[sale['nmId']] = [new_sale]
        logging.info(new_sales)
        if not sending:
            return
        total_new_sales = len(new_sales)
        for employee in db_request.get_employee(seller_id=seller.id):
            if any([employee.order_notif_end, employee.order_notif_ending, employee.order_notif_commission, employee.order_notif_favorites]):
                for _, new_sale_lst in new_sales.items():
                    text = None
                    if len(new_sale_lst) == 1:
                        total_new_sales -= 1
                        text, reply_markup = await inline_kb_new_sale(db_request, sale_id=new_sale_lst[0].id, employee=employee, minus_total=total_new_sales, search=True)
                    elif 4 > len(new_sale_lst) > 1:
                        total_new_sales -= 1
                        text, reply_markup = await inline_kb_new_sale(db_request, sale_id=new_sale_lst[0].id, employee=employee, minus_total=total_new_sales)
                        if text:
                            text += '\n➕ в том числе 👇🏻\n\n'
                            for addit_sale in new_sale_lst[1:]:
                                total_new_sales -= 1
                                text += await inline_kb_new_sale_addit(db_request, sale_id=addit_sale.id, minus_total=total_new_sales)
                    else:
                        if len(new_sale_lst) % 3 == 0:
                            range_num = int(len(new_sale_lst) / 3)
                        else:
                            range_num = int(len(new_sale_lst) / 3) + 1

                        for i in range(range_num):
                            total_new_sales -= 1
                            search = None if len(new_sale_lst[i*3+1 : i*3+3]) > 0 else True
                            text, reply_markup = await inline_kb_new_sale(db_request, sale_id=new_sale_lst[i*3].id, employee=employee, minus_total=total_new_sales, search=search)
                            
                            if text:
                                if not search:
                                    text += '\n➕ в том числе 👇🏻\n\n'
                                    for addit_sale in new_sale_lst[i*3+1 : i*3+3]:
                                        total_new_sales -= 1
                                        text += await inline_kb_new_sale_addit(db_request, sale_id=addit_sale.id, minus_total=total_new_sales)
                                user = db_request.get_user(id=employee.user.id)
                                
                                try:
                                    photo = FSInputFile(f'bot/database/images/{addit_sale.nmId}.jpg', 'rb')
                                    await bot.send_photo(user.tg_id, photo=photo, caption=text, reply_markup=reply_markup)
                                except Exception as ex:
                                    logging.warning(ex)
                        return
                    if text:
                        user = db_request.get_user(id=employee.user.id)
                        try:
                            photo = FSInputFile(f'bot/database/images/{new_sale_lst[0].nmId}.jpg', 'rb')
                            await bot.send_photo(user.tg_id, photo=photo, caption=text, reply_markup=reply_markup)
                        except Exception as ex:
                            logging.warning(ex)



async def update_sellers():
    while True:
        tasks = set()
        db_request = DbRequests()
        for seller in db_request.get_seller():
            if seller.is_active:
                task = asyncio.create_task(update_seller(seller))
                tasks.add(task)
            elif not seller.activation_date:
                if await Statistics.check_orders(db_request, seller, period='today'):
                    # если в течение последних 100 дней были заказы активируем продавца
                    db_request.update_seller(id=seller.id, is_active=True, activation_date=datetime.now())
                    task = asyncio.create_task(update_seller(seller, tariff=True))
                    tasks.add(task)

        results = await asyncio.gather(*tasks)
        logging.info(f'tasks update_sellers created: {datetime.now()}')
        await asyncio.sleep(900)



async def update_seller(seller, tariff : bool = None):
    db_request = DbRequests()
    start = datetime.now()
    if tariff:
        last_month_orders = len(await Statistics.get_orders(db_request, seller, per_month=True))
        if last_month_orders <= 300:
            tariff = 290
        elif 300 < last_month_orders <= 1000:
            tariff = 490
        elif 1000 < last_month_orders <= 3000:
            tariff = 790
        elif 3000 < last_month_orders <= 10000:
            tariff = 1090
        elif 10000 < last_month_orders <= 100000:
            tariff = 1390
        elif last_month_orders > 100000:
            tariff = 1690
        db_request.update_seller(id=seller.id, tariff=tariff)

    sending = True if not tariff else False

    #try:
    await update_stocks(db_request, seller)
    #except Exception as ex:
    #logging.warning(f'{seller} stock ex - {ex}')


    #try:
    await update_orders(db_request, seller, sending=sending)
    #except Exception as ex:
    #logging.warning(f'{seller} orders ex - {ex}')


    try:
        await update_sales(db_request, seller, sending=sending)
    except Exception as ex:
        logging.warning(f'{seller} sales ex - {ex}')


    end = datetime.now()
    logging.info(f'{seller.name}[{seller.id}] finished. Time: {end-start}')
        