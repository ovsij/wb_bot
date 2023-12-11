import aiohttp
import asyncio
from datetime import datetime
import logging
import pandas as pd

from bot.database.functions.db_requests import DbRequests

logging.basicConfig(level=logging.INFO)

async def main(start_num):
    db_request = DbRequests()
    keywords_df = pd.read_csv('bot/database/requests.csv', names=['keyword', 'requests'])
    
    while True:
        try:
            logging.info('Starting...')
            start = datetime.now()
            async with aiohttp.ClientSession(trust_env=True) as session:
                for num in range(start_num, 1001):
                    logging.info(f'Processing batch {num}')
                    tasks = []
                    for i in range((num - 1) * 1000, num * 1000):
                        keyword = [keywords_df.iloc[i]['keyword'], keywords_df.iloc[i]['requests']]
                        tasks.append(asyncio.create_task(get_request(keyword, session, i)))
                    
                    results = await asyncio.gather(*tasks, return_exceptions=True)
                    filtered_results = [result for result in results if isinstance(result, dict)]
                    db_request.create_keyword(keywords=filtered_results)
                    logging.info(f'Added into db: {(num - 1) * 1000} : {num * 1000}: {datetime.now()}')
            
            end = datetime.now()
            logging.info(f'Finished batch. Time taken: {end - start}')
        
        except Exception as e:
            logging.error(f'Error occurred: {e}')
            await asyncio.sleep(60)
        else:
            break

async def get_request(keyword, session, i):
    url = 'https://search.wb.ru/exactmatch/ru/common/v4/search'
    params_first = {'TestGroup': 'control', 'TestID':356, 'appType':1, 'curr': 'rub', 'dest': -1257786, 'filters': 'xsubject', 'query':keyword[0], 'resultset': 'filters'}
    
    try:
        async with session.get(url, params=params_first, ssl=False) as response:
            result = await response.json(content_type='text/plain')
            total = result['data']['total']
    except Exception as e:
        #logging.error(f'Error fetching total: {e}')
        total = 0
    
    products = []
    for page in range(1, 4):
        params_second = {'TestGroup': 'control', 'TestID':356, 'appType':1, 'curr': 'rub', 'dest': -1257786, 'page': page, 'query':str(keyword[0]), 'resultset': 'catalog', 'sort':'popular', 'spp': 26, 'suppressSpellcheck': 'false'}
        try:
            async with session.get(url, params=params_second, ssl=False) as response:
                if response.status == 200:
                    result = await response.json(content_type='text/plain')
                    page_products = [p['id'] for p in result['data']['products']]
                    products.append(page_products)
        except Exception as e:
            logging.error(f'Error fetching products: {e}')
    
    if len(products) == 3:
        return {'keyword': keyword[0], 'requests' :keyword[1], 'search_1': products[0], 'search_2': products[1], 'search_3': products[2], 'total': total}
    return {}

"""import aiohttp, asyncio
from datetime import datetime
import concurrent.futures
import logging
import pandas as pd
import requests
import time
from tqdm import tqdm



from bot.database.functions.db_requests import DbRequests
logging.basicConfig(level=logging.INFO)

async def main(start_num):
    while True:
        logging.info('start')
        db_request = DbRequests()
        
        keywords_df = pd.read_csv('bot/database/requests.csv', names=['keyword', 'requests'])
        logging.info('keywords extracted from file')
        
        start = datetime.now()
        session = aiohttp.ClientSession(trust_env=True)
        for num in range(start_num, 1001):
            try:
                logging.info(f'i: {num}')
                time = datetime.now()
                logging.info(f'start: {(num - 1) * 1000} : {num * 1000}')
                logging.info(f'time: {time}')
                tasks = set()
                for i in range((num - 1) * 1000, num * 1000):
                    keyword = [keywords_df.iloc[i]['keyword'], keywords_df.iloc[i]['requests']]
                    tasks.add(asyncio.create_task(get_request(keyword, start, session, i)))
                results = await asyncio.gather(*tasks)
                db_request.create_keyword(keywords=results)
                logging.info(f'Added into db: {(num - 1) * 1000} : {num * 1000}')
            except:
                await asyncio.sleep(60)
                await main(num)

        await session.close()
        
        end = datetime.now()
        logging.info(f'Finish time {end-start}')
            

async def get_request(keyword, start, session, i):
    
    url = 'https://search.wb.ru/exactmatch/ru/common/v4/search'
    params_first = {'TestGroup': 'control', 'TestID':356, 'appType':1, 'curr': 'rub', 'dest': -1257786, 'filters': 'xsubject', 'query':keyword[0], 'resultset': 'filters'}
    try:
        async with session.get(url, params=params_first, ssl=False) as response:
            result = await response.json(content_type='text/plain')
            total = result['data']['total']
        
    except:
        total = 0
        
    products = []
    for page in range(1, 4):
        params_second = {'TestGroup': 'control', 'TestID':356, 'appType':1, 'curr': 'rub', 'dest': -1257786, 'page': page, 'query':str(keyword[0]), 'resultset': 'catalog', 'sort':'popular', 'spp': 26, 'suppressSpellcheck': 'false'}
        try:
            async with session.get(url, params=params_second, ssl=False) as response:
                if response.status == 200:
                    result = await response.json(content_type='text/plain')
                    page_products = [p['id'] for p in result['data']['products']]
                    products.append(page_products)
                else:
                    pass
           
        except:
            pass
    if len(products) == 3:
        return {'keyword': keyword[0], 'requests' :keyword[1], 'search_1': products[0], 'search_2': products[1], 'search_3': products[2], 'total': total}
"""

if __name__ == '__main__':
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:  # 'RuntimeError: There is no current event loop...'
        loop = None

    if loop and loop.is_running():
        logging.info('Async event loop already running. Adding coroutine to the event loop.')
        tsk = loop.create_task(main())
    else:
        logging.info('Starting new event loop')
        result = asyncio.run(main(1))
