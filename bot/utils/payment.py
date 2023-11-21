import asyncio
from datetime import date, datetime, timedelta
import logging

from bot import bot
from bot.keyboards import *
from bot.database.functions.db_requests import DbRequests


DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

async def regular_payment():
    logging.info(f'regular_payment start: {datetime.now()}')
    while True:
        try:
            db_request = DbRequests()
            tasks = set()
            for seller in db_request.get_seller(test_period=False):
                try:
                    if (datetime.now() - seller.last_payment_date) > timedelta(hours=23.5):
                        task = asyncio.create_task(payment(db_request, seller))
                        tasks.add(task)
                except:
                    if not seller.is_active:
                        task = asyncio.create_task(payment(db_request, seller))
                        tasks.add(task)
            await asyncio.gather(*tasks)
            logging.info(f'tasks regular_payment created: {datetime.now()}')
        except Exception as ex:
            logging.info(ex)
        await asyncio.sleep(1800)
            

async def payment(db_request, seller):
    users = db_request.get_employee(seller_id=seller.id, balance=True)
    send_message = False
    if len(users) > 0:
        for employee in users:
            if employee.is_admin:
                paymet_sum = round(seller.tariff / DAYS[datetime.now().month - 1], 2)
                if db_request.get_user(id=employee.user.id).balance >= paymet_sum:
                    db_request.create_transaction(user_id=employee.user.id, 
                                                sum=paymet_sum, 
                                                type=False,
                                                tariff=f'{seller.tariff}₽/мес',
                                                seller_name=seller.name, 
                                                )
                    db_request.update_seller(id=seller.id, is_active=True, last_payment_date=datetime.now())
                    logging.info(f'User {employee} paid {paymet_sum}')
                    continue
        try:
            seller = db_request.get_seller(id=seller.id)
            if (datetime.now() - seller.last_payment_date) > timedelta(hours=23.5):
                db_request.update_seller(id=seller.id, is_active=False)
                send_message = True
        except:
            pass
    else:
        db_request.update_seller(id=seller.id, is_active=False)
        send_message = True
    if send_message:
        text, reply_markup = inline_kb_cancel_seller(seller)
        for employee in users:
            user = db_request.get_user(id=employee.user.id)
            await bot.send_message(chat_id=user.tg_id, text=text, reply_markup=reply_markup)
                


async def regular_check_test_period():
    logging.info(f'regular_check_test_period start: {datetime.now()}')
    while True:
        db_request = DbRequests()
        # iterate all sellers in test period
        tasks = set()
        for seller in db_request.get_seller(test_period=True):
            task = asyncio.create_task(check_test_period(db_request, seller))
            tasks.add(task)
        await asyncio.gather(*tasks)
        logging.info(f'tasks regular_check_test_period created: {datetime.now()}')
        await asyncio.sleep(1800)
            

async def check_test_period(db_request, seller):
    # if there is less than 30 minutes till cancel of test period
    if (datetime.now() - seller.activation_date) > timedelta(hours=48): #335.5
        db_request.update_seller(id=seller.id, test_period=False, is_active=False)
        # create transaction from first employee who have enough money
        employees = db_request.get_employee(seller_id=seller.id)
        for employee in employees:
            if employee.is_admin:
                user = db_request.get_user(id=employee.user.id)
                paymet_sum = round(seller.tariff / DAYS[datetime.now().month - 1], 2)
                if user.balance >= paymet_sum:
                    db_request.create_transaction(user_id=user.id, 
                                                  sum=paymet_sum, 
                                                  type=False, 
                                                  tariff=f'{seller.tariff}₽/мес',
                                                  seller_name=seller.name, )
                    db_request.update_seller(id=seller.id, is_active=True, last_payment_date=datetime.now())
                    logging.info(f'User {employee} paid {paymet_sum}')
                    break

        seller = db_request.get_seller(id=seller.id)
        if not seller.last_payment_date:
            #db_request.update_seller(id=seller.id, is_active=False)
            text, reply_markup = inline_kb_cancel_seller(seller)
            for employee in employees:
                user = db_request.get_user(id=employee.user.id)
                await bot.send_message(chat_id=user.tg_id, text=text, reply_markup=reply_markup)
            
    

