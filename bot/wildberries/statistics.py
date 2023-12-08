import asyncio, aiohttp
import logging
from datetime import date, datetime, timedelta

class Statistics:
    async def get_reportDetailByPeriod(token):
        headers = {'Authorization': token}
        async with aiohttp.ClientSession(headers=headers, trust_env=True) as session:
            url = 'https://statistics-api.wildberries.ru/api/v1/supplier/reportDetailByPeriod'
            datetime_now = datetime.now()
            params = {'dateFrom': (datetime_now - timedelta(days=10)).strftime('%Y-%m-%d'), 'dateTo': datetime_now.strftime('%Y-%m-%d')}
            await asyncio.sleep(1)
            async with session.get(url, params=params, ssl=False) as response:
                print(await response.text())
                if response.status == 200:
                    result = await response.json()
                    print('200')
                    print(result)
                    return result
                else:
                    print('not 200')
                    logging.info(response)
                    return False

    async def get_stocks(seller, i=1):
        headers = {'Authorization': seller.token}
        async with aiohttp.ClientSession(headers=headers, trust_env=True) as session:
            url = 'https://statistics-api.wildberries.ru/api/v1/supplier/stocks'
            params = {'dateFrom': '2019-06-20'}
            async with session.get(url, params=params, ssl=False) as response:
                if response.status == 200:
                    result = await response.json()
                    return result
                else:
                    await asyncio.sleep(15)
                    print(f'Заказы {seller} Попытка {i}')
                    return await Statistics.get_stocks(seller, i=i+1)
    
    async def get_orders(db_request, seller, per_month = None, i = 1):
        headers = {'Authorization': seller.token}
        async with aiohttp.ClientSession(headers=headers, trust_env=True) as session:
            url = 'https://statistics-api.wildberries.ru/api/v1/supplier/orders'
            orders = db_request.get_order(seller_id=seller.id)
            try:
                params = {'dateFrom': max(o.date for o in orders).strftime('%Y-%m-%d')}
            except:
                params = {'dateFrom': (date.today() - timedelta(days=1000)).strftime('%Y-%m-%d')}
            
            if per_month:
                params = {'dateFrom': (date.today() - timedelta(days=30)).strftime('%Y-%m-%d')}
            await asyncio.sleep(1)
            async with session.get(url, params=params, ssl=False) as response:
                if response.status == 200:
                    result = await response.json()
                    return result
                elif response.status == 401:
                    print(f'Orders {seller} Unauthorized response')
                else:
                    print(f'{seller} orders list is empty')
            
                    await asyncio.sleep(5)
                    print(f'Заказы {seller} Попытка {i}')
                    return await Statistics.get_orders(db_request, seller, i=i+1)
    
    async def get_sales(db_request, seller):
        headers = {'Authorization': seller.token}
        async with aiohttp.ClientSession(headers=headers, trust_env=True) as session:
            url = 'https://statistics-api.wildberries.ru/api/v1/supplier/sales'
            sales = db_request.get_sale(seller_id=seller.id)
            try:
                params = {'dateFrom': max(s.date for s in sales).strftime('%Y-%m-%d')}
            except:
                params = {'dateFrom': (date.today() - timedelta(days=1000)).strftime('%Y-%m-%d')}
            async with session.get(url, params=params, ssl=False) as response:
                if response.status == 200:
                    result = await response.json()
                    return result
                elif response.status == 401:
                    print(f'Sales {seller} Unauthorized response')
                else:
                    print(f'{seller} sales list is empty')
                    print(response)
                    await asyncio.sleep(10)
                    return await Statistics.get_sales(db_request, seller)
    
    async def check_orders(db_request, seller, period : str = None):
        headers = {'Authorization': seller.token}
        async with aiohttp.ClientSession(headers=headers, trust_env=True) as session:
            url = 'https://statistics-api.wildberries.ru/api/v1/supplier/sales'
            timedelta_list = [1, 7, 31, 100] if not period else [1]
            for i in timedelta_list:
                params = {'dateFrom': (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')}
                async with session.get(url, params=params, ssl=False) as response:
                    if response.status == 200:
                        result = await response.json()
                        if len(result) > 0:
                            return True
                    else:
                        print('bad request check_orders')
                        await asyncio.sleep(3)
                        return await Statistics.check_orders(db_request, seller)
                    
    async def get_nomenclature(db_request, seller, supplierArticle):
        headers = {'Authorization': seller.token}
        async with aiohttp.ClientSession(headers=headers, trust_env=True) as session:
            url = 'https://suppliers-api.wildberries.ru/content/v1/cards/filter'
            params = {'vendorCodes': supplierArticle, 'allowedCategoriesOnly' : 'true'}
            async with session.get(url, params=params, ssl=False) as response:
                print(response)
                if response.status == 200:
                    result = await response.json()
                    print(result)