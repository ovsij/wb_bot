import asyncio
from datetime import date, datetime, timedelta

from bot.database.functions.db_requests import DbRequests

DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

async def regular_payment():
    print('regular_payment start')
    while True:
        db_request = DbRequests()
        tasks = set()
        for user in db_request.get_user(balance=True):
            task = asyncio.create_task(payment(db_request, user))
            tasks.add(task)
        await asyncio.gather(*tasks)
        print('tasks regular_payment created')
        await asyncio.sleep(1800)
            

async def payment(db_request, user):
    sellers = db_request.get_seller(user_id=user.id, test_period=False)
    for seller in sellers:
        if (datetime.now() - seller.last_payment_date) > timedelta(hours=23.5):
            employee = db_request.get_employee(user_id=user.id, seller_id=seller.id)
            if employee.is_admin:
                if user.balance >= seller.tariff:
                    paymet_sum = round(seller.tariff / DAYS[datetime.now().month - 1], 2)
                    print(round(seller.tariff / DAYS[datetime.now().month - 1], 2))
                    db_request.create_transaction(user_id=user.id, 
                                                  sum=paymet_sum, 
                                                  type=False,
                                                  tariff=f'{seller.tariff}₽/мес',
                                                  seller_name=seller.name, 
                                                  )
                    db_request.update_seller(id=seller.id, last_payment_date=datetime.now())
                    print(f'User {user} paid')


async def regular_check_test_period():
    print('regular_check_test_period start')
    while True:
        db_request = DbRequests()
        # iterate all sellers in test period
        tasks = set()
        for seller in db_request.get_seller(test_period=True):
            task = asyncio.create_task(check_test_period(db_request, seller))
            tasks.add(task)
        await asyncio.gather(*tasks)
        print('tasks regular_check_test_period created')
        await asyncio.sleep(1800)
            

async def check_test_period(db_request, seller):
    # if there is less than 30 minutes till cancel of test period
    if (datetime.now() - seller.activation_date) > timedelta(hours=335.5):
        db_request.update_seller(id=seller.id, test_period=False, is_active=False)
        # create transaction from first employee who have enough money
        for employee in db_request.get_employee(seller_id=seller.id):
            if employee.is_admin:
                user = db_request.get_user(id=employee.user.id)
                if user.balance >= seller.tariff:
                    paymet_sum = round(seller.tariff / DAYS[datetime.now().month - 1], 2)
                    db_request.create_transaction(user_id=user.id, sum=paymet_sum, type=False)
                    db_request.update_seller(id=seller.id, last_payment_date=datetime.now())
                    break
            
    

