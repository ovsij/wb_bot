from aiogram.types import Message
from datetime import datetime, timedelta
from decimal import Decimal
from pony.orm import *
from secrets import token_hex

from bot.database.enum import *


db = Database()


class User(db.Entity):
    __table_name__ = "users"

    id = PrimaryKey(int, auto=True)
    tg_id = Optional(str, unique=True)
    username = Optional(str, unique=True)
    first_name = Optional(str, nullable=True)
    last_name = Optional(str, nullable=True)
    was_registered = Optional(datetime, default=datetime.now())
    last_use = Optional(datetime, default=datetime.now())
    is_admin = Optional(bool, default=False)
    refer = Optional("User", reverse="referals", nullable=True)
    referals = Set("User", reverse="refer")
    coupons = Set("Coupon")
    balance = Optional(float, default=0)
    transactions = Set("Transaction")
    sellers = Set("User_Seller")
    logs = Set("Log")
    export_token = Optional(str, default=token_hex(15))
    stock_sorting = Optional(StockSorting, default=StockSorting.stockDESC)
    reports_groupby = Optional(ReportsGroupBy, default=ReportsGroupBy.WITHOUTGROUP)
    reports_groupby_period = Optional(ReportsGroupByPeriod, default=ReportsGroupByPeriod.WITHOUTGROUP)


class Seller(db.Entity):
    __table_name__ = "sellers"

    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    token = Required(str)
    token_fbs = Optional(str)
    dragon = Optional(bool, default=True)
    export = Optional(bool, default=True)
    tariff = Optional(int, default=290)
    is_active = Optional(bool, default=False)
    activation_date = Optional(datetime, nullable=True)
    last_payment_date = Optional(datetime, nullable=True)
    test_period = Optional(bool, default = False)
    chat_id = Optional(str, nullable=True)
    products = Set("Product")
    users = Set("User_Seller")


class User_Seller(db.Entity):
    __table_name__ = 'user_seller'

    id = PrimaryKey(int, auto=True)
    user = Required(User)
    seller = Required(Seller)
    is_admin = Optional(bool, default=True)
    is_orders = Optional(bool, default=True)
    is_pay = Optional(bool, default=True)
    is_key_words = Optional(bool, default=True)
    is_article = Optional(bool, default=True) #True - ссылкой, False - текстом + ссылкой
    stock_reserve = Optional(int, default=14)
    is_selected = Optional(bool, default=True)
    order_notif_end = Optional(bool, default=True)
    order_notif_ending = Optional(bool, default=True)
    order_notif_commission = Optional(bool, default=True)
    order_notif_favorites = Optional(bool, default=True)
    buyout_notif_end = Optional(bool, default=True)
    buyout_notif_ending = Optional(bool, default=True)
    buyout_notif_commission = Optional(bool, default=True)
    buyout_notif_favorites = Optional(bool, default=True)
    cancel_notif = Optional(bool, default=True)
    favorites = Set("Product", table="favorites")
    archive = Set("Product", table="archive")
    exportmains = Set("ExportMain")


class Product(db.Entity):
    __table_name__ = "products"

    id = PrimaryKey(int, auto=True)
    seller = Required(Seller)
    warehouses = Set("Product_Warehouse")
    orders = Set("Order")
    sales = Set("Sale")
    in_favorites = Set(User_Seller, reverse='favorites')
    in_archive = Set(User_Seller, reverse="archive")
    supplierArticle = Optional(str) # Артикул продавца
    nmId = Optional(int) # Артикул WB
    barcode = Optional(str) # Баркод
    category = Optional(str) # Категория
    subject = Optional(str) # Предмет
    brand = Optional(str) # Бренд
    techSize = Optional(str) # Размер
    price = Optional(int) # Цена
    discount = Optional(int) # Скидка
    isSupply = Optional(bool) # Договор поставки (внутренние технологические данные)
    isRealization = Optional(bool) # Договор реализации (внутренние технологические данные)
    SCCode = Optional(bool) # Код контракта (внутренние технологические данные)
    rating = Optional(float)
    reviews = Optional(int)

class Order(db.Entity):
    __table_name__ = "orders"

    id = PrimaryKey(int, auto=True)
    product = Required(Product)
    warehouse = Required("Warehouse")
    sale = Optional("Sale")
    gNumber = Optional(str)
    date = Optional(datetime)
    lastChangeDate = Optional(datetime)
    supplierArticle = Optional(str)
    techSize = Optional(str)
    barcode = Optional(str)
    totalPrice = Optional(float)
    discountPercent = Optional(int)
    warehouseName = Optional(str)
    oblast = Optional(str)
    incomeID = Optional(int)
    odid = Optional(int, size=64)
    nmId = Optional(int)
    subject = Optional(str)
    category = Optional(str)
    brand = Optional(str)
    isCancel = Optional(bool)
    cancel_dt = Optional(datetime)
    sticker = Optional(str)
    srid = Optional(str)
    orderType = Optional(str)

class Sale(db.Entity):
    __table_name__ = "sales"

    id = PrimaryKey(int, auto=True)
    product = Required(Product)
    warehouse = Required("Warehouse")
    order = Optional("Order", nullable=True)
    gNumber = Optional(str)
    date = Optional(datetime)
    lastChangeDate = Optional(datetime)
    supplierArticle = Optional(str)
    techSize = Optional(str)
    barcode = Optional(str)
    totalPrice = Optional(float)
    discountPercent = Optional(int)
    isSupply = Optional(bool)
    isRealization = Optional(bool)
    promoCodeDiscount = Optional(int)
    warehouseName = Optional(str)
    countryName = Optional(str)
    oblastOkrugName = Optional(str)
    regionName = Optional(str)
    incomeID = Optional(int)
    saleID = Optional(str)
    odid = Optional(int, size=64)
    spp = Optional(float)
    forPay = Optional(float)
    finishedPrice = Optional(float)
    priceWithDisc = Optional(float)
    nmId = Optional(int)
    subject = Optional(str)
    category = Optional(str)
    brand = Optional(str)
    isStorno = Optional(int)
    sticker = Optional(str)
    srid = Optional(str)

class Warehouse(db.Entity):
    __table_name__ = "warehouses"

    id = PrimaryKey(int, auto=True)
    warehouseName = Optional(str)
    products = Set("Product_Warehouse")
    orders = Set(Order)
    sales = Set(Sale)


class Product_Warehouse(db.Entity):
    __table_name__ = "products_warehouse"

    id = PrimaryKey(int, auto=True)
    product = Required(Product)
    warehouse = Required(Warehouse)
    quantity = Optional(int, nullable=True)
    inWayToClient = Optional(int, nullable=True)
    inWayFromClient = Optional(int, nullable=True)
    quantity_full = Optional(int, nullable=True)


class News(db.Entity):
    __table_name__ = "news"

    id = PrimaryKey(int, auto=True)
    text = Required(str)
    publication_date = Optional(datetime, default=datetime.now())


class Log(db.Entity):
    __table_name__ = "logs"

    id = PrimaryKey(int, auto=True)
    user = Required(User)
    action = Required(str)
    datetime = Required(datetime, default=datetime.now())


class Coupon(db.Entity):
    __table_name__ = "coupones"

    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    sum = Required(int)
    users = Set(User)


class Transaction(db.Entity):
    __table_name__ = "transactions"

    id = PrimaryKey(int, auto=True)
    sum = Required(float)
    user = Required(User)
    type = Required(bool) # True - пополнение (credit), False - списание (debit)
    tariff = Optional(str, nullable=True)
    seller_name = Optional(str, nullable=True)
    balance = Optional(float, nullable=True)
    bill_number = Optional(int)
    bill_link = Optional(str, nullable=True)
    datetime = Required(datetime, default=datetime.now())


class KeyWord(db.Entity):
    __table_name__ = "keyword"

    id = PrimaryKey(int, auto=True)
    keyword = Required(str)
    requests = Optional(int, nullable=True)
    search_1 = Optional(IntArray, nullable=True)
    search_2 = Optional(IntArray, nullable=True)
    search_3 = Optional(IntArray, nullable=True)
    total = Optional(int, nullable=True)
    is_today = Optional(bool, default=True)

class ExportMain(db.Entity):
    __table_name__ = "exportmain"

    id = PrimaryKey(int, auto=True)
    employee = Optional(User_Seller)
    nmId_size = Optional(str)
    nmId = Optional(int)
    size = Optional(str)
    seller_name = Optional(str)
    product_name = Optional(str)
    quantity = Optional(int)
    quantity_till = Optional(int)
    orders_90 = Optional(int)
    orders_30 = Optional(int)
    orders_14 = Optional(int)
    stock_reserve = Optional(int)
    forsupply_14 = Optional(int)
    forsupply_N = Optional(int)
    sales_90 = Optional(int)
    buyout = Optional(int)
    rating = Optional(float)
    updatet_at = Optional(datetime)
    abc_percent = Optional(float)
    abc = Optional(str)

class Comission(db.Entity):
    __table_name__ = "comission"

    id = PrimaryKey(int, auto=True)
    category = Optional(str)
    subject = Optional(str, unique=True)
    percent = Optional(int)
