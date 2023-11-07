import asyncio
from datetime import datetime
import concurrent.futures
import requests
import time
from tqdm import tqdm


from bot.database.functions.db_requests import DbRequests


def main():
    print('start')
    db_request = DbRequests()
    keywords = db_request.get_keywords()
    print('keywords extracted from db')
    
    start = datetime.now()
    #async with aiohttp.ClientSession(trust_env=True) as session:
    #session = aiohttp.ClientSession(trust_env=True)
    session = requests.Session()

    #tasks = set()
    #for keyword in keywords[:10000]:

    CONNECTIONS = 100

    with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
        futures = [executor.submit(get_request_classic, keyword) for keyword in keywords[20000:100000]]
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(keywords[20000:100000])):
            try:
                data = future.result() 
                db_request.update_keyword(id=data['keyword'], search=data['search'], total=data['total'])
            except Exception as exc:   
                print(exc) 
                time.sleep(60)
                print('waiting for 60 seconds')



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

if __name__ == '__main__':
    main()
