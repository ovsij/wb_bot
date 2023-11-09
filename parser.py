import aiohttp, asyncio
from datetime import datetime
import concurrent.futures
import logging
import requests
import time
from tqdm import tqdm



from bot.database.functions.db_requests import DbRequests
logging.basicConfig(level=logging.INFO)

async def main():
    logging.info('start')
    db_request = DbRequests()
    keywords = db_request.get_keywords()
    logging.info('keywords extracted from db')
    
    start = datetime.now()
    session = aiohttp.ClientSession(trust_env=True)
    for i in range(100, 101):
        logging.info(f'i: {i}')
        time = datetime.now()
        logging.info(f'start: {(i - 1) * 10000} : {i * 10000}')
        logging.info(f'time: {time}')
        tasks = set()
        for keyword in keywords[(i - 1) * 10000:i * 10000]:
            tasks.add(asyncio.create_task(get_request(db_request, keyword, start, session)))
        reqults = await asyncio.gather(*tasks)
    await session.close()

    """CONNECTIONS = 4

    with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
        future_to_url = [executor.submit(get_request_classic, keyword) for keyword in keywords[:100000]]
        for future in tqdm(concurrent.futures.as_completed(future_to_url), total=len(keywords[:100000])):
            try:
                data = future.result() 
                db_request.update_keyword(id=data['keyword'], search=data['search'], total=data['total'])
            except Exception as exc:   
                print(exc) """
                
    
            
        #await get_request(db_request, keyword, start, session)
        #tasks.add(asyncio.create_task(get_request(db_request, keyword, start, session)))
    #await asyncio.gather(*tasks)
    #print('tasks created')
    
    end = datetime.now()
    logging.info(f'Time {end-start}')
            

async def get_request(db_request, keyword, start, session):
    url = 'https://search.wb.ru/exactmatch/ru/common/v4/search'
    params_first = {'TestGroup': 'control', 'TestID':351, 'appType':1, 'curr': 'rub', 'dest': -1257786, 'filters': 'xsubject', 'query':keyword[1], 'resultset': 'filters'}
    async with session.get(url, params=params_first, ssl=False) as response:
        try:
            result = await response.json(content_type='text/plain')
            total = result['data']['total']
        except:
            total = 0
        #print(total)
    #print(keyword)
    products = []
    for page in range(1, 4):
        #print(page)
        
        params_second = {'TestGroup': 'control', 'TestID':351, 'appType':1, 'curr': 'rub', 'dest': -1257786, 'page': page, 'query':str(keyword[1]), 'resultset': 'catalog', 'sort':'popular', 'suppressSpellcheck': 'false'}
        async with session.get(url, params=params_second, ssl=False) as response:
            if response.status == 200:
                try:
                    result = await response.json(content_type='text/plain')
                    page_products = [p['id'] for p in result['data']['products']]
                    products.append(page_products)
                    #print(page)
                except:
                    #print(f'{keyword[0]} НЕ ПРОШЕЛ ЗАПРОС!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                    await asyncio.sleep(5)
            else:
                #print(f'{keyword[0]} НЕ ПРОШЕЛ ЗАПРОС!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                await asyncio.sleep(5)
    if len(products) > 0:
        for prod in products:
            db_request.update_keyword(id=keyword[0], search=page_products, total=total, page=products.index(prod)+1)
        


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
        result = asyncio.run(main())
