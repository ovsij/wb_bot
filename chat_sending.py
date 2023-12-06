from datetime import datetime, timedelta
from aiogram.utils.formatting import *
import asyncio
import logging

from bot import bot
from bot.database.functions.db_requests import DbRequests
from bot.utils.utils import get_warehouse_quantity

logging.basicConfig(level=logging.INFO)


async def chat_sendind(db_request):
    chats = db_request.get_seller(chats=True)
    for chat in chats:
        seller = db_request.get_seller(id=chat['id'])
        today_orders = [o['totalPrice'] * (1 - o['discountPercent'] / 100) for o in db_request.get_order(seller_id=seller.id, period='today', select_for='reports')]
        today_sales = [s['priceWithDisc'] for s in db_request.get_sale(seller_id=seller.id, period='today', type='S', select_for='reports')]
        today_returns = [s['priceWithDisc'] for s in db_request.get_sale(seller_id=seller.id, period='today', type='R', select_for='reports')]
        products = db_request.get_product(seller_id=seller.id)
        need_fullfillment = {}
        for product in products:
            orders_90 = db_request.get_order(product_id=product.id, period=f"{(datetime.now() - timedelta(days=90)).strftime('%d.%m.%Y')} - {datetime.now().strftime('%d.%m.%Y')}")
            product_warehouse = db_request.get_product_warehouse(product_id=product.id)
            warehouses, _, quantity_total = get_warehouse_quantity(db_request, orders_90, product_warehouse)
            for name, quantity in warehouses.items():
                try:
                    if quantity[1] < 14:
                        income = int((len(orders_90)/90) * 14 - quantity_total)
                        try:
                            need_fullfillment[product.nmId] += [{name : income}]
                        except:
                            need_fullfillment[product.nmId] = [{name : income}]
                except:
                    ...
        
        text = as_line(f'🥝 {seller.name}',
                            '',
                            Bold('СТАТИСТИКА ЗА СЕГОДНЯ'),
                            f"🛒 Заказы:        {len(today_orders)} на {'{0:,}'.format(int(sum(today_orders))).replace(',', ' ')}₽",
                            f"💳 Выкупы:       {len(today_sales)} на {'{0:,}'.format(int(sum(today_sales))).replace(',', ' ')}₽",
                            f'↩️ Возвраты:    {len(today_returns)}',
                            '',
                            sep='\n')
        
        if len(need_fullfillment) > 0:
            text += as_line('🚗 Необходимо пополнить склады:')
        for article, warehouses in need_fullfillment.items():
            text += as_line(f"Товар ", TextLink(article, url=f"https://www.wildberries.ru/catalog/{article}/detail.aspx"), ':')
            for warehouse in warehouses:
                for name, income in warehouse.items():
                    text += as_line(f'{name} на {income} шт.')

        await bot.send_message(chat_id=int(chat['chat_id']), text=text.as_html())


async def main():
    db_request = DbRequests()
    task1 = asyncio.create_task(chat_sendind(db_request))
    await asyncio.gather(task1)

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
