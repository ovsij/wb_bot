from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse, StreamingResponse
from datetime import datetime, timedelta
import io
import pandas as pd
from pydantic import BaseModel
from string import Template

from bot.database.functions.db_requests import DbRequests
from bot.utils.telegraph import create_page

api = FastAPI()

@api.get('/search/{article}', response_class=HTMLResponse)
def search(article : str):
    db_request = DbRequests()
    keywords = db_request.get_keywords(article=article)
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
    db_request = DbRequests()
    user = db_request.get_user(tg_id=chatID)
    if token == user.export_token:
        sellers_ids = [s.id for s in db_request.get_seller(user_id=user.id) if s.is_active]
        export = []
        for seller_id in sellers_ids:
            exp = db_request.get_exportmain(seller_id) 
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
    db_request = DbRequests()
    user = db_request.get_user(tg_id=chatID)
    if token == user.export_token:
        sellers_ids = [s.id for s in db_request.get_seller(user_id=user.id) if s.is_active]
        products = []
        for seller_id in sellers_ids:
            prod = db_request.get_product(seller_id=seller_id)
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
def orders(chatID, token, search=None, date1=None, date2=None, group=None, group2=None):
    db_request = DbRequests()
    user = db_request.get_user(tg_id=chatID)
    if token == user.export_token:
        if date1:
            period = f"{date1.replace('-', '.')} - {datetime.now().strftime('%d.%m.%Y')}" if not date2 else f"{date1.replace('-', '.')} - {date2.replace('-', '.')}"
        else:
            period = f"{(datetime.now() - timedelta(days=10)).strftime('%d.%m.%Y')} - {datetime.now().strftime('%d.%m.%Y')}"
        sellers_ids = [s.id for s in db_request.get_seller(user_id=user.id) if s.is_active and s.id == 45]
        orders = []
        for seller_id in sellers_ids:
            seller_orders = db_request.get_order(seller_id=seller_id, select_for='reports', period=period, search=search)
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
            print(orders)
                    

            orders = list(orders.values())
            

        df = pd.DataFrame(orders, columns=['', '', '', '', '', '', '', '', '', '', '', '', '', ''])
        stream = io.StringIO()
        df.to_csv(stream, index = False)
        response = StreamingResponse(iter([stream.getvalue()]),
                                    media_type="text/csv"
                                    )
        return response

@api.get('/export/sales')
def sales(chatID, token, search=None, date1=None, date2=None, group=None):
    db_request = DbRequests()
    user = db_request.get_user(tg_id=chatID)
    if token == user.export_token:
        if date1:
            period = f"{date1.replace('-', '.')} - {datetime.now().strftime('%d.%m.%Y')}" if not date2 else f"{date1.replace('-', '.')} - {date2.replace('-', '.')}"
        else:
            period = f"{(datetime.now() - timedelta(days=10)).strftime('%d.%m.%Y')} - {datetime.now().strftime('%d.%m.%Y')}"
        sellers_ids = [s.id for s in db_request.get_seller(user_id=user.id) if s.is_active and s.id == 45]
        orders = []
        for seller_id in sellers_ids:
            seller_sales = db_request.get_sale(seller_id=seller_id, select_for='reports', period=period, search=search, type='S')
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
def return_(chatID, token, search=None, date1=None, date2=None, group=None):
    db_request = DbRequests()
    user = db_request.get_user(tg_id=chatID)
    if token == user.export_token:
        if date1:
            period = f"{date1.replace('-', '.')} - {datetime.now().strftime('%d.%m.%Y')}" if not date2 else f"{date1.replace('-', '.')} - {date2.replace('-', '.')}"
        else:
            period = f"{(datetime.now() - timedelta(days=10)).strftime('%d.%m.%Y')} - {datetime.now().strftime('%d.%m.%Y')}"
        sellers_ids = [s.id for s in db_request.get_seller(user_id=user.id) if s.is_active and s.id == 45]
        orders = []
        for seller_id in sellers_ids:
            seller_sales = db_request.get_sale(seller_id=seller_id, select_for='reports', period=period, search=search, type='R')
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
def penalties(chatID, token, search=None, date1=None, date2=None, group=None):
    db_request = DbRequests()
    user = db_request.get_user(tg_id=chatID)
    if token == user.export_token:
        if date1:
            period = f"{date1.replace('-', '.')} - {datetime.now().strftime('%d.%m.%Y')}" if not date2 else f"{date1.replace('-', '.')} - {date2.replace('-', '.')}"
        else:
            period = f"{(datetime.now() - timedelta(days=10)).strftime('%d.%m.%Y')} - {datetime.now().strftime('%d.%m.%Y')}"
        sellers_ids = [s.id for s in db_request.get_seller(user_id=user.id) if s.is_active and s.id == 45]
        orders = []
        for seller_id in sellers_ids:
            seller_sales = db_request.get_sale(seller_id=seller_id, select_for='reports', period=period, search=search, type='D')
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