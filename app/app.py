from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from string import Template


from database import *

api = FastAPI()


def create_page(requests, article):

    with open('template.html', 'r') as file:
        html_content = file.read()

    url = f'https://www.wildberries.ru/catalog/{article}/detail.aspx'
    rows = ""
    for row in requests:
        page_url = f"https://www.wildberries.ru/catalog/0/search.aspx?page={list(row.values())[0][0]}&sort=popular&search={list(row.keys())[0].replace(' ', '+')}"
        rows += f'<tr><td width="600">{list(row.keys())[0]}</td><td><a href="{page_url}">{list(row.values())[0][0]}-{list(row.values())[0][1]}</a></td><td>0</td><td>{list(row.values())[0][2]}</td><td>{list(row.values())[0][3]}</td></tr>'
    html_content = Template(html_content).substitute(url=url, article=article, rows=rows)
    #with open('test.html', 'w') as file:
    #    file.write(html_content)
    return html_content
        

@db_session()
def get_keyword(article):
    return select(k for k in KeyWord if int(article) in k.search_1 or int(article) in k.search_2 or int(article) in k.search_3 and k.is_today == True)[:]

@db_session()
def get_user(tg_id):
    return User.get(tg_id=tg_id)

@db_session()
def get_product(seller_id):
    return select(p for p in Product if p.seller.id == seller_id)[:]

@api.get('/search/{article}', response_class=HTMLResponse)
def search(article : str):
    keywords = get_keyword(article)
    search_results = []
    for keyword in keywords:
        page_id = 1 if int(article) in keyword.search_1 else 2 if int(article) in keyword.search_2 else 3
        page_list = keyword.search_1 if page_id == 1 else keyword.search_2 if page_id == 2 else keyword.search_3
        index = page_list.index(int(article)) + 1
        search_results.append({keyword.keyword: [page_id, index, keyword.requests, keyword.total]})

    return create_page(requests=search_results, article=article)

class Parameters(BaseModel):
    user : str
    token : str
    search : str
    date1 : str
    date2 : str
    group : bool
    group2 : bool

@api.get('/export/main')
def main(data : Parameters):
    user = get_user(tg_id=user)
    if data.token == user.export_token:
        sellers_ids = [us.seller.id for us in user.seller if us.seller.is_active]
        print(sellers_ids)
        for seller_id in sellers_ids:
            products = get_product(seller_id)

@api.get('/export/subject')
def subject(data : Parameters):
    pass

@api.get('/export/inway')
def inway(data : Parameters):
    pass

@api.get('/export/orders')
def orders(data : Parameters):
    pass

@api.get('/export/sales')
def sales(data : Parameters):
    pass

@api.get('/export/return')
def return_(data : Parameters):
    pass

@api.get('/export/penalties')
def penalties(data : Parameters):
    pass

@api.get('/export/reportDetail')
def reportDetail(data : Parameters):
    pass