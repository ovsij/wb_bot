from aiogram.types import Message
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.enums.parse_mode import ParseMode

from bot.database.database import *
from bot.database.functions.db_requests import DbRequests
from bot.keyboards import *
from bot.wildberries import *
from bot.utils.states import *

user_commands_router = Router()

@user_commands_router.message(Command(commands=["start", "my"]))
async def cmd_start(message: Message, db_request: DbRequests, state: FSMContext):
    print(message.text)
    user = db_request.get_user(tg_id=str(message.from_user.id))
    if db_request.user_seller_exists(user_id=user.id):
        # обработка добавления/удаления в избанное и добвления/удаления товаров в архив
        if 'favorites' in message.text:
            try:
                user = db_request.get_user(tg_id=str(message.from_user.id))
                product = db_request.get_product(id=int(message.text.split('_')[-1]))
                employee = db_request.get_employee(seller_id=product.seller.id, user_id=user.id)
                db_request.update_employee(id=employee.id, favorites=product.id)
                data = await state.get_data()
                text, reply_markup = inline_kb_stock_myproducts(db_request, tg_id=str(message.from_user.id), page=data['page'], filter=data['filter'])
                await data['msg_to_edit'].edit_text(text=text, reply_markup=reply_markup)
            except:
                pass
        elif 'archive' in message.text:
            try:
                user = db_request.get_user(tg_id=str(message.from_user.id))
                product = db_request.get_product(id=int(message.text.split('_')[-1]))
                employee = db_request.get_employee(seller_id=product.seller.id, user_id=user.id)
                db_request.update_employee(id=employee.id, archive=product.id)
                data = await state.get_data()
                text, reply_markup = inline_kb_stock_myproducts(db_request, tg_id=str(message.from_user.id), page=data['page'], filter=data['filter'])
                await data['msg_to_edit'].edit_text(text=text, reply_markup=reply_markup)
            except:
                pass
        # обработка обычного старта если сотрудник уже проходил по ссылке добавления сотрудника
        else:
            text, reply_markup = inline_kb_my(db_request, tg_id=str(message.from_user.id))
            await message.answer(text=text, reply_markup=reply_markup)
    else:
        if message.text in ['/start', '/my']:
            text, reply_markup = inline_kb_start()
            await message.answer(text=text, reply_markup=reply_markup)

        elif 'addemployee' in message.text:
                seller_id = int(message.text.strip('/start ').split('_')[2])
                db_request.update_seller(id=seller_id, user_id=user.id)
                await message.answer('✅ Поздравляем! Успешное подключение.\n🥷🏻 {bot name} работает на вас 🤜🏻')
                text, reply_markup = inline_kb_add_employee(db_request, seller_id=seller_id, tg_id=str(message.from_user.id))
                await message.answer(text=text, reply_markup=reply_markup)
        else:
            await message.answer('Сожалеем, но у вас нет доступа к этому действию...')
    await message.delete()

@user_commands_router.message(Command("balance"))
async def cmd_balance(message: Message, db_request: DbRequests):
    text, reply_markup = inline_kb_balance(db_request, tg_id=str(message.from_user.id))
    await message.answer(text=text, reply_markup=reply_markup)
    await message.delete()

@user_commands_router.message(Command("tariff"))
async def cmd_tariff(message: Message):
    text, reply_markup = inline_kb_tariff()
    await message.answer(text=text, reply_markup=reply_markup)
    await message.delete()

@user_commands_router.message(Command("news"))
async def cmd_news(message: Message, db_request: DbRequests):
    news_ids = [n.id for n in db_request.get_news()]
    if news_ids:
        text, reply_markup = inline_kb_news(db_request, news_id=news_ids[-1], tg_id=str(message.from_user.id))
    else:
        text, reply_markup = inline_kb_news(db_request, tg_id=str(message.from_user.id))
    await message.answer(text=text, reply_markup=reply_markup)
    await message.delete()

@user_commands_router.message(Command("stock"))
async def cmd_stocks(message: Message, db_request: DbRequests):
    """for seller in db_request.get_seller(user_id=db_request.get_user(tg_id=str(message.from_user.id)).id):
        stocks = Statistics.get_stocks(token=seller.token)
        for product in stocks:
            rating, reviews = WbParser.get_rating(article=product['nmId'])
            db_request.create_product(seller_id=seller.id,
                                      supplierArticle=product['supplierArticle'],
                                      nmId=product['nmId'],
                                      barcode=product['barcode'],
                                      category=product['category'],
                                      subject=product['subject'],
                                      brand=seller.name,
                                      techSize=product['techSize'],
                                      price=product['Price'],
                                      discount=product['Discount'],
                                      isSupply=product['isSupply'],
                                      isRealization=product['isRealization'],
                                      SCCode=product['SCCode'],
                                      warehouseName=product['warehouseName'],
                                      quantity=product['quantity'],
                                      inWayToClient=product['inWayToClient'],
                                      inWayFromClient=product['inWayFromClient'],
                                      quantityFull=product['quantityFull'],
                                      rating=rating,
                                      reviews=reviews)"""
            
    text, reply_markup = inline_kb_stocks(db_request, tg_id=str(message.from_user.id))
    await message.answer(text=text, reply_markup=reply_markup)
    await message.delete()    

@user_commands_router.message(Command("reports"))
async def cmd_stocks(message: Message, db_request: DbRequests):
    
    """#await message.delete()
    for seller in db_request.get_seller(user_id=db_request.get_user(tg_id=str(message.from_user.id)).id):
        orders = Statistics.get_orders(db_request, seller)
        start = datetime.now()
        db_orders = [db_request.create_order(gNumber=order['gNumber'],
                                    date=order['date'],
                                    lastChangeDate=order['lastChangeDate'],
                                    supplierArticle=order['supplierArticle'],
                                    techSize=order['techSize'],
                                    barcode=order['barcode'],
                                    totalPrice=order['totalPrice'],
                                    discountPercent=order['discountPercent'],
                                    warehouseName=order['warehouseName'],
                                    oblast=order['oblast'],
                                    incomeID=order['incomeID'],
                                    odid=order['odid'],
                                    nmId=order['nmId'],
                                    subject=order['subject'],
                                    category=order['category'],
                                    brand=order['brand'],
                                    isCancel=order['isCancel'],
                                    cancel_dt=order['cancel_dt'],
                                    sticker=order['sticker'],
                                    srid=order['srid'],
                                    orderType=order['orderType'],) for order in orders]
        end = datetime.now()
        print(f'orders {end-start}')
        sales = Statistics.get_sales(db_request, seller)
        for sale in sales:
            db_request.create_sale(gNumber=sale['gNumber'],
                                   date=sale['date'],
                                   lastChangeDate=sale['lastChangeDate'],
                                   supplierArticle=sale['supplierArticle'],
                                   techSize=sale['techSize'],
                                   barcode=sale['barcode'],
                                   totalPrice=sale['totalPrice'],
                                   discountPercent=sale['discountPercent'], 
                                   isSupply=sale['isSupply'],
                                   isRealization=sale['isRealization'],
                                   warehouseName=sale['warehouseName'], 
                                   countryName=sale['countryName'], 
                                   oblastOkrugName=sale['oblastOkrugName'], 
                                   regionName=sale['regionName'], 
                                   incomeID=sale['incomeID'], 
                                   saleID=sale['saleID'], 
                                   odid=sale['odid'], 
                                   spp=sale['spp'], 
                                   forPay=sale['forPay'], 
                                   finishedPrice=sale['finishedPrice'], 
                                   priceWithDisc=sale['priceWithDisc'], 
                                   nmId=sale['nmId'], 
                                   subject=sale['subject'], 
                                   category=sale['category'], 
                                   brand=sale['brand'], 
                                   sticker=sale['sticker'], 
                                   srid=sale['srid'], )
    start = datetime.now()"""
    text, reply_markup = inline_kb_reports(db_request, tg_id=str(message.from_user.id))
    await message.answer(text=text, reply_markup=reply_markup)
    #end = datetime.now()
    #print(f'Finish total: {end-start}')
    