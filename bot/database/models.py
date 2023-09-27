from aiogram.types import Message
from datetime import datetime, timedelta
from decimal import Decimal
from enum import Enum
from pony.orm import *

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
    balance = Optional(int, default=0)
    transactions = Set("Transaction")
    sellers = Set("User_Seller")
    logs = Set("Log")


class Seller(db.Entity):
    __table_name__ = "sellers"

    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    token = Required(str)
    token_fbs = Optional(str)
    dragon = Optional(bool, default=True)
    export = Optional(bool, default=True)
    tariff = Optional(int, default=490)
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
    order_notif_end = Optional(bool, default=True)
    order_notif_ending = Optional(bool, default=True)
    order_notif_commission = Optional(bool, default=True)
    order_notif_favorites = Optional(bool, default=True)
    buyout_notif_end = Optional(bool, default=True)
    buyout_notif_ending = Optional(bool, default=True)
    buyout_notif_commission = Optional(bool, default=True)
    buyout_notif_favorites = Optional(bool, default=True)
    cancel_notif = Optional(bool, default=True)


class Product(db.Entity):
    __table_name__ = "products"

    id = PrimaryKey(int, auto=True)
    seller = Required(Seller)
    storages = Set("Product_Storage")
    orders = Set("Order")
    

class Order(db.Entity):
    __table_name__ = "orders"

    id = PrimaryKey(int, auto=True)
    product = Required(Product)
    storage = Required("Storage")


class Storage(db.Entity):
    __table_name__ = "storages"

    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    products = Set("Product_Storage")
    orders = Set("Order")


class Product_Storage(db.Entity):
    __table_name__ = "products_storages"
    id = PrimaryKey(int, auto=True)
    product = Required(Product)
    storage = Required(Storage)
    quantity = Optional(int, nullable=True)
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
    sum = Required(int)
    user = Required(User)
    type = Required(bool) # True - пополнение (credit), False - списание (debit)
    bill_number = Optional(int)
    bill_link = Required(str)
    datetime = Required(datetime, default=datetime.now())