from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse, StreamingResponse
from datetime import datetime, timedelta, date
import io
import pandas as pd
from pydantic import BaseModel
import re
from string import Template

from .database import *

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
    return html_content
    #with open('test.html', 'w') as file:
    #    file.write(html_content)

@db_session()
def get_keywords(article=None, is_today=None):
    if article:
        return select(k for k in KeyWord if int(article) in k.search_1 or int(article) in k.search_2 or int(article) in k.search_3 if k.is_today == is_today)[:]

@db_session()
def get_user(id: int = None, 
                tg_id: str = None, 
                username : str = None,
                seller_id : int = None, 
                refer_id : int = None, 
                is_admin : bool = None, 
                date : str = None, 
                coupon_id : int = None, 
                balance : bool = None, ):
    if id:
        user = User[id]
    elif tg_id:
        user = User.get(tg_id=tg_id)
    elif username:
        user = User.get(username=username)
    elif seller_id:
        user = select(u.user for u in User_Seller if u.seller == Seller[seller_id])[:]
    elif refer_id:
        user = list(User[refer_id].referals)
    elif is_admin:
        user = select(u for u in User if u.is_admin)[:]
    elif date == 'week':
        now = datetime.now()
        user = select(u for u in User if now - u.was_registered >= timedelta(days=7) and now - u.last_use >= timedelta(days=7))[:]
    elif coupon_id:
        user = select(u for u in User if Coupon[coupon_id] in u.coupons)[:]
    elif balance:
        user = select(u for u in User if u.balance > 0)[:]
    else:
        user = select(u for u in User)[:]
    
    return user

@db_session()
def get_seller(id : int = None, user_id : int = None, test_period : bool = None):
    if id:
        return Seller[id]
    elif user_id:
        if test_period == False:
            return select(s.seller for s in User[user_id].sellers if not s.seller.test_period)[:]
        else:
            return select(s.seller for s in User[user_id].sellers)[:]
    elif test_period != None:
        return select(s for s in Seller if s.test_period == test_period)[:]
    else:
        return select(s for s in Seller)[:]
    
@db_session()
def get_exportmain(employee_id):
    return select(ex for ex in ExportMain if ex.employee.id == employee_id)[:]

@db_session()
def get_product(id : int = None, seller_id : int = None, nmId : str = None, in_favorites : int = None, in_archive : int = None):
    if id:
        return Product[id]
    elif seller_id and not nmId:
        seller_id = [seller_id] if type(seller_id) == int else seller_id
        return select(p for p in Product if p.seller in (s for s in Seller if s.id in seller_id))[:]
    elif nmId and seller_id:
        return Product.get(nmId=nmId)
    elif in_favorites:
        return select(p for p in Product if User_Seller[in_favorites] in p.in_favorites)[:]
    elif in_archive:
        return select(p for p in Product if User_Seller[in_archive] in p.in_archive)[:]


@db_session()
def get_order(id : int = None, odid : int = None, gNumber : int = None, seller_id : int = None, product_id : int = None, period : str = None, select_for : str = None, tg_id : str = None, search : str = None):
    if id:
        return Order[id]
    elif odid:
        return Order.get(odid=odid)
    elif gNumber:
        return Order.get(gNumber=gNumber)
    elif seller_id:
        if select_for == 'reports':
            if period == 'today':
                query = select((o.id, o.totalPrice, o.discountPercent, o.subject, o.nmId, o.brand, o.oblast, o.category, o.supplierArticle) for o in Order if o.product.seller == Seller[seller_id] and o.date.date() == date.today())[:]
            elif period == 'yesterday':
                query = select((o.id, o.totalPrice, o.discountPercent, o.subject, o.nmId, o.brand, o.oblast, o.category, o.supplierArticle) for o in Order if o.product.seller == Seller[seller_id] and o.date.date() == date.today() - timedelta(days=1))[:]
            elif period == 'week':
                query = select((o.id, o.totalPrice, o.discountPercent, o.subject, o.nmId, o.brand, o.oblast, o.category, o.supplierArticle) for o in Order if o.product.seller == Seller[seller_id] and o.date.date() >= date.today() - timedelta(days=8) and o.date.date() != date.today())[:]
            elif period == 'month':
                query = select((o.id, o.totalPrice, o.discountPercent, o.subject, o.nmId, o.brand, o.oblast, o.category, o.supplierArticle) for o in Order if o.product.seller == Seller[seller_id] and o.date.date() >= date.today() - timedelta(days=31) and o.date.date() != date.today())[:]
            elif re.fullmatch('\d*.\d*.\d*', period):
                query = select((o.id, o.totalPrice, o.discountPercent, o.subject, o.nmId, o.brand, o.oblast, o.category, o.supplierArticle) for o in Order if o.product.seller == Seller[seller_id] and o.date.date() == datetime.strptime(period, '%d.%m.%Y'))[:]
            elif re.fullmatch('\d*.\d*.\d* - \d*.\d*.\d*', period):
                datefrom = datetime.strptime(period.split(' - ')[0], '%d.%m.%Y')
                dateto = datetime.strptime(period.split(' - ')[1], '%d.%m.%Y')
                if search: # для гугл таблиц
                    query = select((o.id, o.totalPrice, o.discountPercent, o.subject, o.nmId, o.brand, o.oblast, o.category, o.supplierArticle, o.techSize, o.date, o.srid, o.warehouseName) for o in Order if o.product.seller == Seller[seller_id] and o.date.date() >= datefrom and o.date.date() <= dateto and str(o.odid) == search or str(o.nmId) == search or str(o.supplierArticle) == search)[:]
                else:
                    query = select((o.id, o.totalPrice, o.discountPercent, o.subject, o.nmId, o.brand, o.oblast, o.category, o.supplierArticle, o.techSize, o.date, o.srid, o.warehouseName) for o in Order if o.product.seller == Seller[seller_id] and o.date.date() >= datefrom and o.date.date() <= dateto)[:]
            else:
                query = select((o.id, o.totalPrice, o.discountPercent, o.subject, o.nmId, o.brand, o.oblast, o.category, o.supplierArticle) for o in Order if o.product.seller == Seller[seller_id])[:]
            return [{'totalPrice': q[1], 'discountPercent': q[2], 'subject': q[3], 'nmId': q[4], 'brand': q[5], 'oblast': q[6], 'category': q[7], 'supplierArticle': q[8], 'techSize': q[9], 'date': q[10], 'srid': q[11], 'warehouseName': q[12]} for q in query]
        else:
            if period == 'today':
                return select(o for o in Order if o.product.seller == Seller[seller_id] and o.date.date() == date.today())[:]
            elif period == 'yesterday':
                return select(o for o in Order if o.product.seller == Seller[seller_id] and o.date.date() == date.today() - timedelta(days=1))[:]
            elif period == 'week':
                return select(o for o in Order if o.product.seller == Seller[seller_id] and o.date.date() >= date.today() - timedelta(days=8) and o.date.date() != date.today())[:]
            elif period == 'month':
                return select(o for o in Order if o.product.seller == Seller[seller_id] and o.date.date() >= date.today() - timedelta(days=31) and o.date.date() != date.today())[:]
            else:
                return select(o for o in Order if o.product.seller == Seller[seller_id])[:]
    elif product_id:
        if re.fullmatch('\d*.\d*.\d* - \d*.\d*.\d*', period):
            datefrom = datetime.strptime(period.split(' - ')[0], '%d.%m.%Y')
            dateto = datetime.strptime(period.split(' - ')[1], '%d.%m.%Y')
            query = select((o.id, o.totalPrice, o.discountPercent, o.gNumber, o.date, o.nmId, o.warehouseName) for o in Order if o.product.id == product_id and o.date.date() >= datefrom and o.date.date() <= dateto)[:]
            return [{'id': q[0], 'totalPrice': q[1], 'discountPercent': q[2], 'gNumber': q[3], 'date': q[4], 'nmId': q[5], 'warehouse' : q[6]} for q in query]
    elif tg_id:
        user = User.get(tg_id=tg_id)
        sellers = select(us.seller for us in user.sellers if us.is_selected)[:]
        query = select((o.id, o.date, o.totalPrice, o.discountPercent, o.srid, o.nmId, o.subject, o.brand, o.supplierArticle, o.oblast, o.warehouseName) for o in Order if o.product.seller in sellers).order_by(lambda: desc(o.date))[:]
        return [{'date': q[1], 'totalPrice': q[2], 'discountPercent': q[3], 'srid': q[4], 'nmId': q[5], 'subject': q[6], 'brand': q[7], 'supplierArticle': q[8], 'oblast': q[9], 'warehouseName': q[10]} for q in query]

@db_session()
def get_sale(id : int = None, odid : int = None, seller_id : int = None, product_id : int = None, period : str = None, type : str = None, select_for : str = None, tg_id : str = None, search : str = None):
    if id:
        return Sale[id]
    elif odid:
        return Sale.get(odid=odid)
    elif seller_id:
        if select_for == 'reports':
            if period == 'today':
                query = select((s.id, s.priceWithDisc, s.subject, s.nmId, s.brand, s.regionName, s.category, s.supplierArticle) for s in Sale if s.product.seller == Seller[seller_id] and s.date.date() == date.today() and s.saleID.startswith(type))[:]
            elif period == 'yesterday':
                query = select((s.id, s.priceWithDisc, s.subject, s.nmId, s.brand, s.regionName, s.category, s.supplierArticle) for s in Sale if s.product.seller == Seller[seller_id] and s.date.date() == date.today() - timedelta(days=1) and s.saleID.startswith(type))[:]
            elif period == 'week':
                query = select((s.id, s.priceWithDisc, s.subject, s.nmId, s.brand, s.regionName, s.category, s.supplierArticle) for s in Sale if s.product.seller == Seller[seller_id] and s.date.date() >= date.today() - timedelta(days=8) and s.date.date() != date.today() and s.saleID.startswith(type))[:]
            elif period == 'month':
                query = select((s.id, s.priceWithDisc, s.subject, s.nmId, s.brand, s.regionName, s.category, s.supplierArticle) for s in Sale if s.product.seller == Seller[seller_id] and s.date.date() >= date.today() - timedelta(days=31) and s.date.date() != date.today() and s.saleID.startswith(type))[:]
            elif re.fullmatch('\d*.\d*.\d*', period):
                query = select((s.id, s.priceWithDisc, s.subject, s.nmId, s.brand, s.regionName, s.category, s.supplierArticle) for s in Sale if s.product.seller == Seller[seller_id] and s.date.date() == datetime.strptime(period, '%d.%m.%Y') and s.saleID.startswith(type))[:]
            elif re.fullmatch('\d*.\d*.\d* - \d*.\d*.\d*', period):
                datefrom = datetime.strptime(period.split(' - ')[0], '%d.%m.%Y')
                dateto = datetime.strptime(period.split(' - ')[1], '%d.%m.%Y')
                if search: # для гугл таблиц
                    query = select((s.id, s.priceWithDisc, s.subject, s.nmId, s.brand, s.regionName, s.category, s.supplierArticle, s.techSize, s.date, s.srid, s.warehouseName) for s in Sale if s.product.seller == Seller[seller_id] and s.date.date() >= datefrom and s.date.date() <= dateto and s.saleID.startswith(type) and str(o.odid) == search or str(o.nmId) == search or str(o.supplierArticle) == search)[:]
                else:
                    query = select((s.id, s.priceWithDisc, s.subject, s.nmId, s.brand, s.regionName, s.category, s.supplierArticle, s.techSize, s.date, s.srid, s.warehouseName) for s in Sale if s.product.seller == Seller[seller_id] and s.date.date() >= datefrom and s.date.date() <= dateto and s.saleID.startswith(type))[:]
            else:
                return select(s for s in Sale if s.product.seller == Seller[seller_id] and s.saleID.startswith(type))[:]
            return [{'priceWithDisc': q[1], 'subject': q[2], 'nmId': q[3], 'brand': q[4], 'regionName': q[5], 'category': q[6], 'supplierArticle': q[7], 'techSize': q[8], 'date': q[9], 'srid': q[10], 'warehouseName': q[11]} for q in query]
        else:
            if period == 'today':
                return select(s for s in Sale if s.product.seller == Seller[seller_id] and s.date.date() == date.today())[:]
            elif period == 'yesterday':
                return select(s for s in Sale if s.product.seller == Seller[seller_id] and s.date.date() == date.today() - timedelta(days=1))[:]
            elif period == 'week':
                return select(s for s in Sale if s.product.seller == Seller[seller_id] and s.date.date() >= date.today() - timedelta(days=8) and s.date.date() != date.today())[:]
            elif period == 'month':
                return select(s for s in Sale if s.product.seller == Seller[seller_id] and s.date.date() >= date.today() - timedelta(days=31) and s.date.date() != date.today())[:]
            else:
                return select(s for s in Sale if s.product.seller == Seller[seller_id])[:]
    elif product_id:
        if re.fullmatch('\d*.\d*.\d* - \d*.\d*.\d*', period):
            datefrom = datetime.strptime(period.split(' - ')[0], '%d.%m.%Y')
            dateto = datetime.strptime(period.split(' - ')[1], '%d.%m.%Y')
            query = select((s.id, s.priceWithDisc, s.gNumber, s.nmId, s.spp) for s in Sale if s.product.id == product_id and s.date.date() >= datefrom and s.date.date() <= dateto and s.saleID.startswith(type) and s.order)[:]
            return [{'priceWithDisc': q[1], 'gNumber': q[2], 'nmId': q[3], 'spp': q[4]} for q in query]
    elif tg_id:
        user = User.get(tg_id=tg_id)
        sellers = select(us.seller for us in user.sellers if us.is_selected)[:]
        query = select((s.id, s.date, s.priceWithDisc, s.srid, s.nmId, s.subject, s.brand, s.supplierArticle, s.regionName, s.warehouseName) for s in Sale if s.product.seller in sellers and s.saleID.startswith(type)).order_by(lambda: desc(s.date))[:]
        return [{'date': q[1], 'priceWithDisc': q[2], 'srid': q[3], 'nmId': q[4], 'subject': q[5], 'brand': q[6], 'supplierArticle': q[7], 'oblast': q[8], 'warehouseName': q[9]} for q in query]

@db_session
def get_employee(user_id):
    return select(u for u in User_Seller if u.seller.is_active and u.user.id == user_id)[:]


@api.get('/search/{article}', response_class=HTMLResponse)
def search(article : str):
    keywords = get_keywords(article=article)
    search_results = []
    for keyword in keywords:
        page_id = 1 if int(article) in keyword.search_1 else 2 if int(article) in keyword.search_2 else 3
        page_list = keyword.search_1 if page_id == 1 else keyword.search_2 if page_id == 2 else keyword.search_3
        index = page_list.index(int(article)) + 1
        search_results.append({keyword.keyword: [page_id, index, keyword.requests, keyword.total]})

    return create_page(requests=search_results, article=article)

BOT_VERSION = 'WbConviergeBot v.0.1'


@api.get('/export/main')
def main(chatID, token):
    user = get_user(tg_id=chatID)
    if token == user.export_token:
        employee_ids = [e.id for e in get_employee(user_id=user.id)]
        export = []
        for employee_id in employee_ids:
            exp = get_exportmain(employee_id) 
            for ex in exp:
                export.append([ex.nmId_size, ex.nmId, ex.size,  ex.seller_name, ex.product_name, ex.quantity, ex.quantity_till, ex.orders_90, ex.orders_30, ex.orders_14, ex.stock_reserve, ex.forsupply_14, ex.forsupply_N, ex.sales_90, ex.buyout, ex.rating, ex.updatet_at, ex.abc_percent, ex.abc])   
        
        
        df = pd.DataFrame(export, columns=['загружено', BOT_VERSION, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])
        stream = io.StringIO()
        df.to_csv(stream, index = False)
        response = StreamingResponse(iter([stream.getvalue()]),
                                    media_type="text/csv"
                                    )
        return response

@api.get('/export/subject')
def subject(chatID, token):
    user = get_user(tg_id=chatID)
    if token == user.export_token:
        sellers_ids = [s.id for s in get_seller(user_id=user.id) if s.is_active]
        products = []
        for seller_id in sellers_ids:
            prod = get_product(seller_id=seller_id)
            for p in prod:
                size = p.techSize if p.techSize != '0' else ''
                products.append([f"{p.nmId}_{size}", p.nmId, p.techSize, p.category, p.subject, p.supplierArticle, p.brand])

        df = pd.DataFrame(products, columns=['', '', '', '', '', '', ''])
        stream = io.StringIO()
        df.to_csv(stream, index = False)
        response = StreamingResponse(iter([stream.getvalue()]),
                                    media_type="text/csv"
                                    )
        return response

@api.get('/export/inway')
def inway(data):
    pass

@api.get('/export/orders')
def orders(chatID, token, search=None, date1=None, date2=None, group : bool = None, group2=None, r=None):
    user = get_user(tg_id=chatID)
    if token == user.export_token:
        if date1:
            period = f"{date1.replace('-', '.')} - {datetime.now().strftime('%d.%m.%Y')}" if not date2 else f"{date1.replace('-', '.')} - {date2.replace('-', '.')}"
        else:
            period = f"{(datetime.now() - timedelta(days=10)).strftime('%d.%m.%Y')} - {datetime.now().strftime('%d.%m.%Y')}"
        sellers_ids = [s.id for s in get_seller(user_id=user.id) if s.is_active]
        orders = []
        for seller_id in sellers_ids:
            seller_orders = get_order(seller_id=seller_id, select_for='reports', period=period, search=search)
            for s_o in seller_orders:
                size = s_o['techSize'] if s_o['techSize'] != '0' else ''
                orders.append([f"{s_o['nmId']}_{size}", s_o['date'].strftime('%d-%m-%Y'), s_o['srid'], s_o['date'], s_o['subject'], s_o['category'], s_o['nmId'], size, s_o['supplierArticle'], 1, int(s_o['totalPrice'] * (1 - s_o['discountPercent'] / 100)), s_o['warehouseName'], s_o['oblast'], s_o['brand']])
        orders.sort(key=lambda x: x[3], reverse=True)
        if group and not group2:
            orders_for_group = orders
            orders = {}
            for order in orders_for_group:
                try:
                    orders[order[6]][9] += 1
                    orders[order[6]][10] += order[10]
                except:
                    order[2] = 'группа'
                    order[11] = 'группа'
                    order[12] = 'группа'
                    orders[order[6]] = order
            orders = list(orders.values())
        elif group2:
            orders_for_group = orders
            orders = {}
            for order in orders_for_group:
                try:
                    orders[f'{order[6]}-{order[1]}'][2] += 1
                    orders[f'{order[6]}-{order[1]}'][3] += order[10]
                    
                except:
                    
                    new_order = [order[0], order[1], order[9], order[10], '', '', '', '', '', '', '', '', '', '']
                    orders[f'{order[6]}-{order[1]}'] = new_order
            orders = list(orders.values())
            

        df = pd.DataFrame(orders, columns=['', '', '', '', '', '', '', '', '', '', '', '', '', ''])
        stream = io.StringIO()
        df.to_csv(stream, index = False)
        response = StreamingResponse(iter([stream.getvalue()]),
                                    media_type="text/csv"
                                    )
        return response

@api.get('/export/sales')
def sales(chatID, token, search=None, date1=None, date2=None, group : bool = None):
    user = get_user(tg_id=chatID)
    if token == user.export_token:
        if date1:
            period = f"{date1.replace('-', '.')} - {datetime.now().strftime('%d.%m.%Y')}" if not date2 else f"{date1.replace('-', '.')} - {date2.replace('-', '.')}"
        else:
            period = f"{(datetime.now() - timedelta(days=10)).strftime('%d.%m.%Y')} - {datetime.now().strftime('%d.%m.%Y')}"
        sellers_ids = [s.id for s in get_seller(user_id=user.id) if s.is_active]
        orders = []
        for seller_id in sellers_ids:
            seller_sales = get_sale(seller_id=seller_id, select_for='reports', period=period, search=search, type='S')
            for s_o in seller_sales:
                size = s_o['techSize'] if s_o['techSize'] != '0' else ''
                orders.append([f"{s_o['nmId']}_{size}", s_o['date'].strftime('%d-%m-%Y'), s_o['srid'], s_o['date'], s_o['subject'], s_o['category'], s_o['nmId'], size, s_o['supplierArticle'], 1, s_o['priceWithDisc'], s_o['warehouseName'], s_o['regionName'], s_o['brand']])
        orders.sort(key=lambda x: x[3], reverse=True)

        if group:
            orders_for_group = orders
            orders = {}
            for order in orders_for_group:
                try:
                    orders[order[6]][9] += 1
                    orders[order[6]][10] += order[10]
                    orders[order[6]][3] = period
                except:
                    order[2] = 'группа'
                    order[11] = 'группа'
                    order[12] = 'группа'
                    orders[order[6]] = order
                    orders[order[6]][3] = period
            orders = list(orders.values())
            

        df = pd.DataFrame(orders, columns=['', '', '', '', '', '', '', '', '', '', '', '', '', ''])
        stream = io.StringIO()
        df.to_csv(stream, index = False)
        response = StreamingResponse(iter([stream.getvalue()]),
                                    media_type="text/csv"
                                    )
        return response

@api.get('/export/return')
def return_(chatID, token, search=None, date1=None, date2=None, group : bool = None):
    user = get_user(tg_id=chatID)
    if token == user.export_token:
        if date1:
            period = f"{date1.replace('-', '.')} - {datetime.now().strftime('%d.%m.%Y')}" if not date2 else f"{date1.replace('-', '.')} - {date2.replace('-', '.')}"
        else:
            period = f"{(datetime.now() - timedelta(days=10)).strftime('%d.%m.%Y')} - {datetime.now().strftime('%d.%m.%Y')}"
        sellers_ids = [s.id for s in get_seller(user_id=user.id) if s.is_active]
        orders = []
        for seller_id in sellers_ids:
            seller_sales = get_sale(seller_id=seller_id, select_for='reports', period=period, search=search, type='R')
            for s_o in seller_sales:
                size = s_o['techSize'] if s_o['techSize'] != '0' else ''
                orders.append([f"{s_o['nmId']}_{size}", s_o['date'].strftime('%d-%m-%Y'), s_o['srid'], s_o['date'], s_o['subject'], s_o['category'], s_o['nmId'], size, s_o['supplierArticle'], 1, s_o['priceWithDisc'], s_o['warehouseName'], s_o['regionName'], s_o['brand']])
        orders.sort(key=lambda x: x[3], reverse=True)

        if group:
            orders_for_group = orders
            orders = {}
            for order in orders_for_group:
                try:
                    orders[order[6]][9] += 1
                    orders[order[6]][10] += order[10]
                    orders[order[6]][3] = period
                except:
                    order[2] = 'группа'
                    order[11] = 'группа'
                    order[12] = 'группа'
                    orders[order[6]] = order
                    orders[order[6]][3] = period
            orders = list(orders.values())
            

        df = pd.DataFrame(orders, columns=['', '', '', '', '', '', '', '', '', '', '', '', '', ''])
        stream = io.StringIO()
        df.to_csv(stream, index = False)
        response = StreamingResponse(iter([stream.getvalue()]),
                                    media_type="text/csv"
                                    )
        return response

@api.get('/export/penalties')
def penalties(chatID, token, search=None, date1=None, date2=None, group : bool = None):
    user = get_user(tg_id=chatID)
    if token == user.export_token:
        if date1:
            period = f"{date1.replace('-', '.')} - {datetime.now().strftime('%d.%m.%Y')}" if not date2 else f"{date1.replace('-', '.')} - {date2.replace('-', '.')}"
        else:
            period = f"{(datetime.now() - timedelta(days=10)).strftime('%d.%m.%Y')} - {datetime.now().strftime('%d.%m.%Y')}"
        sellers_ids = [s.id for s in get_seller(user_id=user.id) if s.is_active]
        orders = []
        for seller_id in sellers_ids:
            seller_sales = get_sale(seller_id=seller_id, select_for='reports', period=period, search=search, type='D')
            for s_o in seller_sales:
                size = s_o['techSize'] if s_o['techSize'] != '0' else ''
                orders.append([f"{s_o['nmId']}_{size}", s_o['date'].strftime('%d-%m-%Y'), s_o['srid'], s_o['date'], s_o['subject'], s_o['category'], s_o['nmId'], size, s_o['supplierArticle'], 1, s_o['priceWithDisc'], s_o['warehouseName'], s_o['regionName'], s_o['brand']])
        orders.sort(key=lambda x: x[3], reverse=True)

        if group:
            orders_for_group = orders
            orders = {}
            for order in orders_for_group:
                try:
                    orders[order[6]][9] += 1
                    orders[order[6]][10] += order[10]
                    orders[order[6]][3] = period
                except:
                    order[2] = 'группа'
                    order[11] = 'группа'
                    order[12] = 'группа'
                    orders[order[6]] = order
                    orders[order[6]][3] = period
            orders = list(orders.values())
            

        df = pd.DataFrame(orders, columns=['', '', '', '', '', '', '', '', '', '', '', '', '', ''])
        stream = io.StringIO()
        df.to_csv(stream, index = False)
        response = StreamingResponse(iter([stream.getvalue()]),
                                    media_type="text/csv"
                                    )
        return response

@api.get('/export/reportDetail')
def reportDetail(data):
    pass