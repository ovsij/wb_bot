import asyncio
from datetime import datetime, timedelta
import logging


from bot.database.functions.db_requests import DbRequests
from bot.utils.abc_analysis import get_abc


async def update(db_request, employee):
    products = db_request.get_product(seller_id=employee.seller.id)
    for p in products:
        start = datetime.now()
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
        
        orders_N = len(db_request.get_order(product_id=p.id, period=f"{(datetime.now() - timedelta(days=employee.stock_reserve)).strftime('%d.%m.%Y')} - {datetime.now().strftime('%d.%m.%Y')}"))
        forsupply_14 = 0 if orders_14 <= stock else int((orders_14 / 14) * 14 - stock)
        forsupply_N = 0 if orders_N <= stock else int((orders_N / 14) * 14 - stock)
        sales_90 = db_request.get_sale(product_id=p.id, period=f"{(datetime.now() - timedelta(days=90)).strftime('%d.%m.%Y')} - {datetime.now().strftime('%d.%m.%Y')}", type='S')
        #buyout
        gnumbers = [s['gNumber'] for s in sales_90]
        
        orders_list = [o for o in orders if o['gNumber'] in gnumbers]
        try:
            buyout = int((len(sales_90) / len(orders_list)) * 100)
        except:
            buyout = 0
        abc, abc_percent = get_abc(db_request, product_id=p.id, seller_id=seller.id)
        result = [f'{p.nmId}_{size}', p.nmId, size, seller.name, p.supplierArticle, stock, quantity_till, orders_90, orders_30, orders_14, employee.stock_reserve, forsupply_14, forsupply_N, len(sales_90), buyout, p.rating, datetime.now().strftime('%d.%m.%Y %H:%M'), abc_percent, abc]
        db_request.create_exportmain(employee_id=employee.id,
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
        

async def update_mainexport():
    logging.info(f'update_mainexport start: {datetime.now()}')
    while True:
        db_request = DbRequests()
        # iterate all sellers in test period
        tasks = set()
        for employee in db_request.get_employee(is_active=True):
            task = asyncio.create_task(update(db_request, employee))
            tasks.add(task)
        await asyncio.gather(*tasks)
        logging.info(f'tasks update_mainexport created: {datetime.now()}')
        await asyncio.sleep(15600)