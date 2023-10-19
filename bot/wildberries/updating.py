import asyncio
from aiogram.types import FSInputFile
from datetime import date, datetime, timedelta

from bot.database.functions.db_requests import DbRequests
from bot.keyboards import *
from bot import bot
from bot.wildberries import *

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

        await asyncio.gather(*tasks)
        print('tasks update_sellers created')
        await asyncio.sleep(1800)

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

    try:
        
        print(f'{seller.name}[{seller.id}] started stocks. Time: {datetime.now()}')
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
                                    brand=seller.name,
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
    except Exception as ex:
        print(ex)
    """UPDATING ORDERS"""
    try:
        print(f'{seller.name}[{seller.id}] started orders. Time: {datetime.now()}')
        orders = await Statistics.get_orders(db_request, seller)
        new_orders = []
        for order in orders:
            new_order = db_request.create_order(gNumber=order['gNumber'],
                                    date=order['date'],
                                    lastChangeDate=order['lastChangeDate'],
                                    supplierArticle=order['supplierArticle'],
                                    techSize=order['techSize'],
                                    barcode=order['barcode'],
                                    totalPrice=order['totalPrice'],
                                    discountPercent=order['discountPercent'],
                                    warehouseName=order['warehouseName'],
                                    oblast=order['oblast'],
                                    incomeID=order['incomeID'],
                                    odid=order['odid'],
                                    nmId=order['nmId'],
                                    subject=order['subject'],
                                    category=order['category'],
                                    brand=order['brand'],
                                    isCancel=order['isCancel'],
                                    cancel_dt=order['cancel_dt'],
                                    sticker=order['sticker'],
                                    srid=order['srid'],
                                    orderType=order['orderType'],)
            #await asyncio.sleep(0.00001)
            if new_order != None:
                new_orders.append(new_order)
        for order in new_orders:
            text = inline_kb_new_order(db_request, order_id=order.id)
            for employee in db_request.get_employee(seller_id=seller.id):
                user = db_request.get_user(id=employee.user.id)
                try:
                    photo = FSInputFile(f'bot/database/images/{order.nmId}.jpg', 'rb')
                    await bot.send_photo(user.tg_id, photo=photo, caption=text)
                except Exception as ex:
                    print(ex)
        
    except Exception as ex:
        print(ex)
    """UPDATING SALES"""
    try:
        print(f'{seller.name}[{seller.id}] started sales. Time: {datetime.now()}')
        sales = await Statistics.get_sales(db_request, seller)
        for sale in sales:
            await db_request.create_sale(gNumber=sale['gNumber'],
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
                                odid=sale['odid'], 
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
            await asyncio.sleep(0.00001)
    except Exception as ex:
        print(ex)


    end = datetime.now()
    print(f'{seller.name}[{seller.id}] finished. Time: {end-start}')
        