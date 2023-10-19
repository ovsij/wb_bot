import asyncio, aiofiles, aiohttp
from bs4 import BeautifulSoup as bs
import requests
import os

class WbParser:
    async def get_rating(article):
        async with aiohttp.ClientSession(trust_env=True) as session:
            async with session.get(f'https://card.wb.ru/cards/detail?appType=1&nm={article}', ssl=False) as response:
                data = await response.json()
                try:
                    rating = data['data']['products'][0]['reviewRating']
                except:
                    rating = 0
                try:
                    reviews = data['data']['products'][0]['feedbacks']
                except:
                    reviews = 0
                return rating, reviews
    
    async def get_image(article):
        if not os.path.exists(f'bot/database/images/{article}.jpg'):
            tasks = set()
            for i in ['12', '11', '10', '06', '05', '04', '07', '08', '09', '03', '02', '01']:
                task = asyncio.create_task(WbParser.download_image(article, i))
                tasks.add(task)
            asyncio.gather(*tasks)
                

    async def download_image(article, i):
        async with aiohttp.ClientSession(trust_env=True) as session:
            article = str(article)
            if article.startswith('1'):
                url = f'https://basket-{i}.wb.ru/vol{article[:4]}/part{article[:6]}/{article}/images/big/1.webp'
            else:
                url = f'https://basket-{i}.wb.ru/vol{article[:3]}/part{article[:5]}/{article}/images/big/1.webp'
            async with session.get(url, ssl=False) as response:
                if response.status == 200:
                    f = await aiofiles.open(f'bot/database/images/{article}.jpg', mode='wb')
                    await f.write(await response.read())
                    await f.close()