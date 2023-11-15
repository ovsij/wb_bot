from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse, StreamingResponse
from datetime import datetime, timedelta
import io
import pandas as pd
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

@db_session()
def get_seller(user_id=None, product_id=None):
    if user_id:
        return select(us.seller for us in User_Seller if us.user == User[user_id])[:]
    if product_id:
        return select(s for s in Seller if Product[product_id] in s.products)[:][0]
    
@db_session()
def get_stock(product_id=None):
    return sum(select(pw.quantity for pw in Product_Warehouse if pw.product == Product[product_id])[:])

@db_session()
def get_order(product_id=None, till=None):
    start = datetime.now()
    query = select((o.gNumber) for o in Order if o.product == Product[product_id] and o.date > datetime.now() - timedelta(days=till))[:]
    end = datetime.now()
    print(f'orders time: {end-start}')
    return [{'gNumber': q} for q in query]


@db_session()
def get_sale(product_id=None, till=None):
    query = select((s.priceWithDisc, s.gNumber) for s in Sale if s.product == Product[product_id] and s.date > datetime.now() -  timedelta(days=till) and s.saleID.startswith('S'))[:]
    return [{'priceWithDisc': q[0], 'gNumber': q[1]} for q in query]

@db_session()
def get_employee(user_id=None, seller_id=None):
    return select(us for us in User_Seller if us.user.id == user_id and us.seller.id == seller_id)[:][0]


def get_abc(product_id, seller_id):
    products = get_product(seller_id=seller_id)
    products_revenue = {}
    total_revenue = 0
    for product_entity in products:
        sales_list = get_sale(product_id=product_entity.id, till=90)
        sales_revenue = sum([s['priceWithDisc'] for s in sales_list])
        products_revenue[product_entity.id] = sales_revenue
        total_revenue += sales_revenue
    
    sorted_products_revenue = sorted(products_revenue.items(), key=lambda item: item[1], reverse=True)

    cummulative_total = 0
    for product, revenue in sorted_products_revenue:
        abc_percent = revenue / total_revenue * 100
        cummulative_total += abc_percent
        if product == product_id:
            if cummulative_total <= 80:
                abc = 'A'
            elif  cummulative_total <= 95:
                abc = 'B'
            else:
                abc = 'C'
            return abc, round(abc_percent, 2)
        
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

BOT_VERSION = 'WbConviergeBot v.0.1'

class Parameters(BaseModel):
    user : str
    token : str
    search : str
    date1 : str
    date2 : str
    group : bool
    group2 : bool

@api.get('/export/main')
def main(chatID, token):
    user = get_user(tg_id=chatID)
    if token == user.export_token:
        sellers_ids = [s.id for s in get_seller(user_id=user.id) if s.is_active]
        products = []
        for seller_id in sellers_ids:
            p = get_product(seller_id)
            products += p
        df_data = [['загружено', BOT_VERSION]]
        for p in products[:3]:
            start = datetime.now()
            print(f'start {p} - {start}')
            size = p.techSize if p.techSize != 0 else ''
            seller = get_seller(product_id=p.id)
            stock = get_stock(product_id=p.id)
            orders = get_order(product_id=p.id, till=1000)
            orders_90 = len(get_order(product_id=p.id, till=90))
            orders_30 = len(get_order(product_id=p.id, till=30))
            orders_14 = len(get_order(product_id=p.id, till=14))
            try:
                quantity_till = int(stock / (orders_90 / 90))
            except:
                quantity_till = 0
            employee = get_employee(user_id=user.id, seller_id=p.seller.id)
            orders_N = len(get_order(product_id=p.id, till=employee.stock_reserve))
            forsupply_14 = 0 if orders_14 <= stock else (orders_14 / 14) * 14 - stock
            forsupply_N = 0 if orders_N <= stock else (orders_N / 14) * 14 - stock
            sales_90 = get_sale(product_id=p.id, till=90)
            #buyout
            gnumbers = [s['gNumber'] for s in sales_90]
            
            orders_list = [o for o in orders if o['gNumber'] in gnumbers]
            try:
                buyout = int((len(sales_90) / len(orders_list)) * 100)
            except:
                buyout = 0
            abc, abc_percent = get_abc(product_id=p.id, seller_id=seller.id)
            result = [f'{p.nmId}_{size}', p.nmId, size, seller.name, p.supplierArticle, stock, quantity_till, orders_90, orders_30, orders_14, employee.stock_reserve, forsupply_14, forsupply_N, len(sales_90), buyout, p.rating, datetime.now().strftime('%d.%m.%Y %H:%M'), abc_percent, abc]
            df_data.append(result)
        df = pd.DataFrame(df_data)
        stream = io.StringIO()
        df.to_csv(stream, index = False)
        response = StreamingResponse(iter([stream.getvalue()]),
                                    media_type="text/csv"
                                    )
        return response

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