from datetime import datetime, date
import logging
import re

from bot.database.database import *
from bot.database.models import *

@db_session()
class DbRequests:
    """"Database requests"""
    @db_session()
    def __init__(self):
        super().__init__()


    """User requests"""
    @db_session()
    def create_user(self, telegram_user, refer_id = None, is_admin = None):
        if not User.exists(tg_id = str(telegram_user.id)):
            user = User(
                tg_id=str(telegram_user.id), 
                username=telegram_user.username, 
                first_name=telegram_user.first_name, 
                last_name=telegram_user.last_name)
            if refer_id:
                user.refer = User[refer_id]
            if is_admin:
                user.is_admin = is_admin
            flush()
            return user
        else:
            print(f'User {telegram_user.id} exists')

    @db_session()
    def get_user(self, id: int = None, 
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
    def update_user(self, id: int = None, tg_id: str = None, updated_fields: dict = None, coupon_id : int = None):
        if id:
            user_to_update = User[id]
        elif tg_id:
            user_to_update = User.get(tg_id=tg_id)
        if updated_fields:
            user_to_update.set(**updated_fields)
        if coupon_id:
            if user_to_update.coupons:
                user_to_update.coupons += Coupon[coupon_id]  
            else:
                user_to_update.coupons = Coupon[coupon_id]  
        return user_to_update
    
    """Seller requests"""
    @db_session()
    def create_seller(self, name : str, user_id : int, token : int):
        if not Seller.exists(token=token):
            seller = Seller(name=name, token=token)
            User_Seller(user=User[user_id], seller=seller)
        else:
            seller = Seller.get(token=token)
            user = User[user_id]
            if not User_Seller.exists(seller=seller, user=user):
                User_Seller(user=user, seller=seller)
        return seller
    
    @db_session()
    def get_seller(self, id : int = None, user_id : int = None, test_period : bool = None, chats : bool = None):
        if id:
            return Seller[id]
        elif user_id:
            if test_period == False:
                return select(s.seller for s in User[user_id].sellers if not s.seller.test_period)[:]
            else:
                return select(s.seller for s in User[user_id].sellers)[:]
        elif test_period != None:
            return select(s for s in Seller if s.test_period == test_period)[:]
        elif chats:
            query = select((s.id, s.chat_id) for s in Seller if s.chat_id)[:]
            return [{'id': q[0], 'chat_id': q[1]} for q in query]
        else:
            return select(s for s in Seller)[:]
        
    
    @db_session()
    def update_seller(self, id : int, 
                      name : str = None, 
                      user_id : int = None,
                      token : str = None,
                      products : list = [],
                      dragon : bool = None, 
                      export : bool = None, 
                      tariff : int = None,
                      is_active : bool = None,
                      activation_date : datetime = None,
                      test_period : bool = None, 
                      last_payment_date : datetime = None, 
                      update_chat : bool = None,
                      chat_id : str = None):
        seller_to_update = Seller[id]
        if name:
            seller_to_update.name = name
        if user_id:
            seller_to_update.users += User_Seller(user=User[user_id], seller=seller_to_update, is_admin=False)
        if token:
            seller_to_update.token = token
        if products:
            seller_to_update.products = products
        if dragon != None:
            seller_to_update.dragon = dragon
        if export != None:
            seller_to_update.export = export
        if tariff != None:
            seller_to_update.tariff = tariff
        if is_active != None:
            seller_to_update.is_active = is_active
        if activation_date:
            seller_to_update.activation_date = activation_date
        if test_period != None:
            seller_to_update.test_period = test_period
        if last_payment_date:
            seller_to_update.last_payment_date = last_payment_date
        if update_chat:
            seller_to_update.chat_id = chat_id
        return seller_to_update
    
    @db_session()
    def delete_seller(self, id : int):
        return Seller[id].delete()
    
    @db_session()
    def seller_exists(self, id : int = None):
        if id:
            return Seller.exists(id=id)
    

    """User_Seller requests"""
    @db_session()
    def user_seller_exists(self, user_id : int = None):
        return User_Seller.exists(user=User[user_id])
    
    @db_session()
    def get_employee(self, id : int = None, seller_id : int = None, user_id : int = None, balance : bool = None, is_active : bool = None):
        if id:
            return User_Seller[id]
        if seller_id and not user_id:
            if balance:
                return select(u for u in User_Seller if u.seller.id == seller_id and u.user.balance > 0)[:]
            else:
                return select(u for u in User_Seller if u.seller.id == seller_id)[:]
        if seller_id and user_id:
            return select(u for u in User_Seller if u.seller.id == seller_id and u.user.id == user_id)[:][0]
        if user_id and not seller_id:
            return select(u for u in User_Seller if u.user.id == user_id)[:]
        if is_active:
            return select(u for u in User_Seller if u.seller.is_active)[:]
    
    @db_session()
    def update_employee(self, id : int, 
                        is_orders : bool = None, 
                        is_pay : bool = None, 
                        is_key_words : bool = None, 
                        is_article : bool = None, 
                        stock_reserve : int = None, 
                        is_selected : bool = None,
                        order_notif_end : bool = None, 
                        order_notif_ending : bool = None, 
                        order_notif_commission : bool = None, 
                        order_notif_favorites : bool = None, 
                        buyout_notif_end : bool = None, 
                        buyout_notif_ending : bool = None, 
                        buyout_notif_commission : bool = None, 
                        buyout_notif_favorites : bool = None, 
                        cancel_notif : bool = None, 
                        favorites : int = None, 
                        archive : int = None):
        
        employee_to_update = User_Seller[id]
        if is_orders != None:
            employee_to_update.is_orders = is_orders
        if is_pay != None:
            employee_to_update.is_pay = is_pay
        if is_key_words != None:
            employee_to_update.is_key_words = is_key_words
        if is_article != None:
            employee_to_update.is_article = is_article
        if stock_reserve != None:
            employee_to_update.stock_reserve = stock_reserve
        if is_selected != None:
            employee_to_update.is_selected = is_selected
        if order_notif_end != None:
            employee_to_update.order_notif_end = order_notif_end
        if order_notif_ending != None:
            employee_to_update.order_notif_ending = order_notif_ending
        if order_notif_commission != None:
            employee_to_update.order_notif_commission = order_notif_commission
        if order_notif_favorites != None:
            employee_to_update.order_notif_favorites = order_notif_favorites
        if buyout_notif_end != None:
            employee_to_update.buyout_notif_end = buyout_notif_end
        if buyout_notif_ending != None:
            employee_to_update.buyout_notif_ending = buyout_notif_ending
        if buyout_notif_commission != None:
            employee_to_update.buyout_notif_commission = buyout_notif_commission
        if buyout_notif_favorites != None:
            employee_to_update.buyout_notif_favorites = buyout_notif_favorites
        if cancel_notif != None:
            employee_to_update.cancel_notif = cancel_notif
        if favorites:
            if Product[favorites] in employee_to_update.favorites:
                employee_to_update.favorites -= Product[favorites]
            else:
                employee_to_update.favorites += Product[favorites]
        if archive:
            if Product[archive] in employee_to_update.archive:
                employee_to_update.archive -= Product[archive]
            else:
                employee_to_update.archive += Product[archive]
                
        return employee_to_update
    
    @db_session()
    def delete_employee(self, id : int):
        return User_Seller[id].delete()
    
    """Transaction requests"""
    @db_session()
    def create_transaction(self, 
                           user_id : int, 
                           sum : float, 
                           type : bool, 
                           tariff : str = None, 
                           seller_name : str = None, 
                           coupon_name : str = None, 
                           bill_link : str = '', 
                           bill_number : int = None):
        user = User[user_id]
        bill_link_ = f'Купон: {coupon_name}' if coupon_name else bill_link        
            
        if type:
            transaction = Transaction(user=user, sum=sum, type=type, bill_link=bill_link_)
            user.balance += sum
        else:
            transaction = Transaction(user=user, sum=sum, type=type, tariff=tariff, seller_name=seller_name, bill_link=bill_link_)
            user.balance -= sum
            transaction.balance = round(user.balance, 2)

        if bill_number:
            transaction.bill_number = bill_number


        return user, transaction
        
    @db_session()
    def get_transaction(self, id : int = None, user_id : int = None, type : bool = None):
        if id:
            return Transaction[id]
        if user_id:
            if type != None:
                return select(t for t in User[user_id].transactions if t.type == type).order_by(lambda: desc(t.datetime))[:10]
            else:
                return select(t for t in User[user_id].transactions)[:]
        
        
    """Coupon requests"""
    @db_session()
    def create_coupon(self, name : str, sum : int):
        return Coupon(name=name, sum=sum)
    
    @db_session()
    def get_coupon(self, id : int = None, name : str = None, user_id : int = None):
        if id:
            return Coupon[id]
        elif name:
            return Coupon.get(name=name)
        elif user_id:
            return select(c for c in Coupon if User[user_id] in c.users)[:]
        else:
            return select(c for c in Coupon)[:]
    
    @db_session()
    def update_coupon(self, sum : str, id : int = None, name : str = None):
        if id:
            coupon_to_update = Coupon[id]
        elif name:
            coupon_to_update = Coupon.get(name=name)

        coupon_to_update.sum = sum
        return coupon_to_update

    @db_session()
    def delete_coupon(self, id : int = None, name : str = None):
        if id:
            coupon_to_delete = Coupon[id]
        elif name:
            coupon_to_delete = Coupon.get(name=name)

        coupon_to_delete.delete()

    """News requests"""
    @db_session()
    def create_news(self, text : str,):
        return News(text=text)
    
    @db_session()
    def get_news(self, id : int = None, ):
        if id:
            return News[id]
        else:
            return select(n for n in News)[:]
    
    @db_session()
    def delete_news(self, id : int, ):
        News[id].delete()

    """Product requests"""
    @db_session()
    async def create_product(self, seller_id : int, 
                       supplierArticle : str, 
                       nmId : int, 
                       barcode : str, 
                       category : str, 
                       subject : str,
                       brand : str, 
                       techSize : str, 
                       price : int, 
                       discount : int, 
                       isSupply : bool, 
                       isRealization : bool, 
                       SCCode : bool,
                       warehouseName : str, 
                       quantity : int, 
                       inWayToClient : int, 
                       inWayFromClient : int, 
                       quantityFull : int, 
                       rating : float,
                       reviews : int, ):
        
        if Product.exists(supplierArticle=supplierArticle, seller=Seller[seller_id]):
            product = Product.get(supplierArticle=supplierArticle, seller=Seller[seller_id])
            product.price = price
            product.discount = discount
            product.rating = rating
            product.reviews = reviews
        else:
            product = Product(seller=Seller[seller_id], 
                              supplierArticle=supplierArticle,
                              nmId=nmId,
                              barcode=barcode,
                              category=category,
                              subject=subject,
                              brand=brand,
                              techSize=techSize,
                              price=price,
                              discount=discount,
                              isSupply=isSupply,
                              isRealization=isRealization,
                              SCCode=SCCode, 
                              rating=rating, 
                              reviews=reviews, )
        
        warehouse = self.get_warehouse(warehouseName=warehouseName)

        if Product_Warehouse.exists(product=product, warehouse=warehouse):
            product_warehouse = Product_Warehouse.get(product=product, warehouse=warehouse)
            product_warehouse.quantity=quantity
            product_warehouse.inWayToClient=inWayToClient
            product_warehouse.inWayFromClient=inWayFromClient
            product_warehouse.quantity_full=quantityFull
        else:
            Product_Warehouse(product=product,
                              warehouse=warehouse,
                              quantity=quantity,
                              inWayToClient=inWayToClient,
                              inWayFromClient=inWayFromClient,
                              quantity_full=quantityFull, )
    
    @db_session()
    def get_product(self, id : int = None, seller_id : int = None, nmId : str = None, in_favorites : int = None, in_archive : int = None):
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
        
    """Warehouse requests"""
    @db_session()
    def get_warehouse(self, id : int = None, warehouseName : str = None, ):
        if id:
            return Warehouse[id]
        else:
            if Warehouse.exists(warehouseName=warehouseName):
                return Warehouse.get(warehouseName=warehouseName)
            else:
                return Warehouse(warehouseName=warehouseName)
        
    """Product_Warehouse requests"""
    @db_session()
    def get_product_warehouse(self,  seller_id : int = None, product_id : int = None, ):
        if seller_id:
            return select(pw for pw in Product_Warehouse if pw.product.seller == Seller[seller_id])[:]
        elif product_id:
            return select(pw for pw in Product_Warehouse if pw.product.id == product_id)[:]

    """Order requests"""
    @db_session()
    def create_order(self, seller_id : str,
                     gNumber : str, 
                     date : datetime, 
                     lastChangeDate : datetime, 
                     supplierArticle : str, 
                     techSize : str, 
                     barcode : str, 
                     totalPrice : float, 
                     discountPercent : int, 
                     warehouseName : str, 
                     oblast : str, 
                     incomeID : int, 
                     #odid : int, 
                     nmId : int, 
                     subject : str, 
                     category : str, 
                     brand : str, 
                     isCancel : bool, 
                     cancel_dt : datetime, 
                     sticker : str, 
                     srid : str, 
                     orderType : str, ):
        
        product = Product.get(barcode=barcode, seller=Seller[seller_id])
        if not product:
            #print(f'product {barcode} не найден')
            return
        
        if not Order.exists(product=product, srid=srid):
            order = Order(product=product, 
                          warehouse=self.get_warehouse(warehouseName=warehouseName), 
                          gNumber=gNumber,
                          date=date,
                          lastChangeDate=lastChangeDate,
                          supplierArticle=supplierArticle,
                          techSize=techSize,
                          barcode=barcode,
                          totalPrice=totalPrice,
                          discountPercent=discountPercent,
                          warehouseName=warehouseName,
                          oblast=oblast,
                          incomeID=incomeID,
                          #odid=odid,
                          nmId=nmId,
                          subject=subject,
                          category=category,
                          brand=product.brand,
                          isCancel=isCancel,
                          cancel_dt=cancel_dt,
                          sticker=sticker,
                          srid=srid,
                          orderType=orderType,
                          )
            flush()
            return order
        else:
            #print(datetime.strptime(date, "%Y-%m-%dT%H:%M:%S"))
            #print(f'order уже есть {srid} ({date})')
            return None
                  
    @db_session()
    def get_order(self, id : int = None, odid : int = None, gNumber : int = None, seller_id : int = None, product_id : int = None, period : str = None, select_for : str = None, tg_id : str = None, search : str = None, warehouse = None, min_date : bool = None):
        if id:
            return Order[id]
        #elif odid:
        #    return Order.get(odid=odid)
        elif gNumber:
            return Order.get(gNumber=gNumber, product=Product[product_id])
        elif seller_id:
            if select_for == 'reports':
                if period == 'today':
                    query = select((o.id, o.totalPrice, o.discountPercent, o.subject, o.nmId, o.brand, o.oblast, o.category, o.supplierArticle, o.techSize, o.date, o.srid, o.warehouseName) for o in Order if o.product.seller == Seller[seller_id] and o.date.date() == date.today())[:]
                elif period == 'yesterday':
                    query = select((o.id, o.totalPrice, o.discountPercent, o.subject, o.nmId, o.brand, o.oblast, o.category, o.supplierArticle, o.techSize, o.date, o.srid, o.warehouseName) for o in Order if o.product.seller == Seller[seller_id] and o.date.date() == date.today() - timedelta(days=1))[:]
                elif period == 'week':
                    query = select((o.id, o.totalPrice, o.discountPercent, o.subject, o.nmId, o.brand, o.oblast, o.category, o.supplierArticle, o.techSize, o.date, o.srid, o.warehouseName) for o in Order if o.product.seller == Seller[seller_id] and o.date.date() >= date.today() - timedelta(days=8) and o.date.date() != date.today())[:]
                elif period == 'month':
                    query = select((o.id, o.totalPrice, o.discountPercent, o.subject, o.nmId, o.brand, o.oblast, o.category, o.supplierArticle, o.techSize, o.date, o.srid, o.warehouseName) for o in Order if o.product.seller == Seller[seller_id] and o.date.date() >= date.today() - timedelta(days=31) and o.date.date() != date.today())[:]
                elif re.fullmatch('\d*.\d*.\d*', period):
                    query = select((o.id, o.totalPrice, o.discountPercent, o.subject, o.nmId, o.brand, o.oblast, o.category, o.supplierArticle, o.techSize, o.date, o.srid, o.warehouseName) for o in Order if o.product.seller == Seller[seller_id] and o.date.date() == datetime.strptime(period, '%d.%m.%Y'))[:]
                elif re.fullmatch('\d*.\d*.\d* - \d*.\d*.\d*', period):
                    datefrom = datetime.strptime(period.split(' - ')[0], '%d.%m.%Y')
                    dateto = datetime.strptime(period.split(' - ')[1], '%d.%m.%Y')
                    if search: # для гугл таблиц
                        query = select((o.id, o.totalPrice, o.discountPercent, o.subject, o.nmId, o.brand, o.oblast, o.category, o.supplierArticle, o.techSize, o.date, o.srid, o.warehouseName) for o in Order if o.product.seller == Seller[seller_id] and o.date.date() >= datefrom and o.date.date() <= dateto and str(o.odid) == search or str(o.nmId) == search or str(o.supplierArticle) == search)[:]
                    else:
                        query = select((o.id, o.totalPrice, o.discountPercent, o.subject, o.nmId, o.brand, o.oblast, o.category, o.supplierArticle, o.techSize, o.date, o.srid, o.warehouseName) for o in Order if o.product.seller == Seller[seller_id] and o.date.date() >= datefrom and o.date.date() <= dateto)[:]
                else:
                    query = select((o.id, o.totalPrice, o.discountPercent, o.subject, o.nmId, o.brand, o.oblast, o.category, o.supplierArticle, o.techSize, o.date, o.srid, o.warehouseName) for o in Order if o.product.seller == Seller[seller_id])[:]
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
            if period:
                if re.fullmatch('\d*.\d*.\d* - \d*.\d*.\d*', period):
                    datefrom = datetime.strptime(period.split(' - ')[0], '%d.%m.%Y')
                    dateto = datetime.strptime(period.split(' - ')[1], '%d.%m.%Y')
                    query = select((o.id, o.totalPrice, o.discountPercent, o.gNumber, o.date, o.nmId, o.warehouseName) for o in Order if o.product.id == product_id and o.date.date() >= datefrom and o.date.date() <= dateto)[:]
                    return [{'id': q[0], 'totalPrice': q[1], 'discountPercent': q[2], 'gNumber': q[3], 'date': q[4], 'nmId': q[5], 'warehouse' : q[6]} for q in query]
            elif warehouse and min_date:
                return select(o.date for o in Order if o.warehouse == warehouse).order_by(lambda: o.date)[:1]
        elif tg_id:
            user = User.get(tg_id=tg_id)
            sellers = select(us.seller for us in user.sellers if us.is_selected)[:]
            query = select((o.id, o.date, o.totalPrice, o.discountPercent, o.srid, o.nmId, o.subject, o.brand, o.supplierArticle, o.oblast, o.warehouseName) for o in Order if o.product.seller in sellers).order_by(lambda: desc(o.date))[:]
            return [{'date': q[1], 'totalPrice': q[2], 'discountPercent': q[3], 'srid': q[4], 'nmId': q[5], 'subject': q[6], 'brand': q[7], 'supplierArticle': q[8], 'oblast': q[9], 'warehouseName': q[10]} for q in query]

    """Sales requests"""
    @db_session()
    def create_sale(self, seller_id : str,
                     gNumber : str, 
                     date : datetime, 
                     lastChangeDate : datetime, 
                     supplierArticle : str, 
                     techSize : str, 
                     barcode : str, 
                     totalPrice : float, 
                     discountPercent : int, 
                     isSupply : bool,
                     isRealization : bool,
                     warehouseName : str, 
                     countryName : str, 
                     oblastOkrugName : str, 
                     regionName : str, 
                     incomeID : int, 
                     saleID : str, 
                     #odid : int, 
                     spp : float, 
                     forPay : float, 
                     finishedPrice : float, 
                     priceWithDisc : float, 
                     nmId : int, 
                     subject : str, 
                     category : str, 
                     brand : str, 
                     sticker : str, 
                     srid : str, ):
        product = Product.get(barcode=barcode, seller=Seller[seller_id])
        if not product:
            return
        if not Sale.exists(saleID=saleID, product=product):
            
            try:
                order = self.get_order(gNumber=gNumber, product=product.id)
            except:
                order = None
            sale = Sale(product=product,
                        warehouse=self.get_warehouse(warehouseName=warehouseName), 
                        order=order,
                        gNumber=gNumber,
                        date=date,
                        lastChangeDate=lastChangeDate,
                        supplierArticle=supplierArticle,
                        techSize=techSize,
                        barcode=barcode,
                        totalPrice=totalPrice,
                        discountPercent=discountPercent, 
                        isSupply=isSupply,
                        isRealization=isRealization,
                        warehouseName=warehouseName, 
                        countryName=countryName, 
                        oblastOkrugName=oblastOkrugName, 
                        regionName=regionName, 
                        incomeID=incomeID, 
                        saleID=saleID, 
                        #odid=odid, 
                        spp=spp, 
                        forPay=forPay, 
                        finishedPrice=finishedPrice, 
                        priceWithDisc=priceWithDisc, 
                        nmId=nmId, 
                        subject=subject, 
                        category=category, 
                        brand=product.brand, 
                        sticker=sticker, 
                        srid=srid, )
            flush()
            return sale
        else:
            return None
        

    @db_session()
    def get_sale(self, id : int = None, odid : int = None, seller_id : int = None, product_id : int = None, period : str = None, type : str = None, select_for : str = None, tg_id : str = None, search : str = None):
        if id:
            return Sale[id]
        elif odid:
            return Sale.get(odid=odid)
        elif seller_id:
            if select_for == 'reports':
                if period == 'today':
                    query = select((s.id, s.priceWithDisc, s.subject, s.nmId, s.brand, s.regionName, s.category, s.supplierArticle, s.techSize, s.date, s.srid, s.warehouseName) for s in Sale if s.product.seller == Seller[seller_id] and s.date.date() == date.today() and s.saleID.startswith(type))[:]
                elif period == 'yesterday':
                    query = select((s.id, s.priceWithDisc, s.subject, s.nmId, s.brand, s.regionName, s.category, s.supplierArticle, s.techSize, s.date, s.srid, s.warehouseName) for s in Sale if s.product.seller == Seller[seller_id] and s.date.date() == date.today() - timedelta(days=1) and s.saleID.startswith(type))[:]
                elif period == 'week':
                    query = select((s.id, s.priceWithDisc, s.subject, s.nmId, s.brand, s.regionName, s.category, s.supplierArticle, s.techSize, s.date, s.srid, s.warehouseName) for s in Sale if s.product.seller == Seller[seller_id] and s.date.date() >= date.today() - timedelta(days=8) and s.date.date() != date.today() and s.saleID.startswith(type))[:]
                elif period == 'month':
                    query = select((s.id, s.priceWithDisc, s.subject, s.nmId, s.brand, s.regionName, s.category, s.supplierArticle, s.techSize, s.date, s.srid, s.warehouseName) for s in Sale if s.product.seller == Seller[seller_id] and s.date.date() >= date.today() - timedelta(days=31) and s.date.date() != date.today() and s.saleID.startswith(type))[:]
                elif re.fullmatch('\d*.\d*.\d*', period):
                    query = select((s.id, s.priceWithDisc, s.subject, s.nmId, s.brand, s.regionName, s.category, s.supplierArticle, s.techSize, s.date, s.srid, s.warehouseName) for s in Sale if s.product.seller == Seller[seller_id] and s.date.date() == datetime.strptime(period, '%d.%m.%Y') and s.saleID.startswith(type))[:]
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
                query = select((s.id, s.priceWithDisc, s.gNumber, s.nmId, s.spp, s.date, s.order) for s in Sale if s.product.id == product_id and s.date.date() >= datefrom and s.date.date() <= dateto and s.saleID.startswith(type))[:]
                return [{'priceWithDisc': q[1], 'gNumber': q[2], 'nmId': q[3], 'spp': q[4], 'date': q[5], 'order': q[6]} for q in query]
        elif tg_id:
            user = User.get(tg_id=tg_id)
            sellers = select(us.seller for us in user.sellers if us.is_selected)[:]
            query = select((s.id, s.date, s.priceWithDisc, s.srid, s.nmId, s.subject, s.brand, s.supplierArticle, s.regionName, s.warehouseName) for s in Sale if s.product.seller in sellers and s.saleID.startswith(type)).order_by(lambda: desc(s.date))[:]
            return [{'date': q[1], 'priceWithDisc': q[2], 'srid': q[3], 'nmId': q[4], 'subject': q[5], 'brand': q[6], 'supplierArticle': q[7], 'oblast': q[8], 'warehouseName': q[9]} for q in query]

    """KeyWord requests"""
    @db_session()
    def create_keyword(self, keywords):
        for keyword in keywords:
            try:
                if KeyWord.exists(keyword=keyword['keyword'], is_today=True):
                    today_keyword = KeyWord.get(keyword=keyword['keyword'], is_today=True)
                    if KeyWord.exists(keyword=keyword['keyword'], is_today=False):
                        yesterday_keyword = KeyWord.get(keyword=keyword['keyword'], is_today=False)
                        yesterday_keyword.requests = today_keyword.requests
                        yesterday_keyword.search_1 = today_keyword.search_1
                        yesterday_keyword.search_2 = today_keyword.search_2
                        yesterday_keyword.search_3 = today_keyword.search_3
                        yesterday_keyword.total = today_keyword.total
                    else:
                        KeyWord(keyword=today_keyword.keyword, requests=today_keyword.requests, search_1=today_keyword.search_1, search_2=today_keyword.search_2, search_3=today_keyword.search_3, total=today_keyword.total, is_today=False)
                    today_keyword.requests = keyword['requests']
                    today_keyword.search_1 = keyword['search_1']
                    today_keyword.search_2 = keyword['search_2']
                    today_keyword.search_3 = keyword['search_3']
                    today_keyword.total = keyword['total']
                else:
                    KeyWord(keyword=keyword['keyword'], requests=keyword['requests'], search_1=keyword['search_1'], search_2=keyword['search_2'], search_3=keyword['search_3'], total=keyword['total'], is_today=True)
            except:
                pass


    @db_session()
    def create_keywords(self):
        import pandas as pd
        df = pd.read_csv('bot/database/requests.csv', names=['keyword', 'requests'])
        for i in range(len(df)):
            try:
                requests = int(df.iloc[i]['requests'])
                
                KeyWord(keyword=str(df.iloc[i]['keyword']), requests=requests)
            except Exception as ex:
                print(ex)
    
    @db_session()
    def update_keyword(self, id=None, search=None, total=None):
    
        pass

    @db_session()
    def get_keyword(self, keyword, is_today):
        return KeyWord.get(keyword=keyword, is_today=is_today)
    

    @db_session()
    def get_keywords(self, article=None, product_card=None, is_today=None):
        if product_card:
            return select(k for k in KeyWord if f' {k.keyword} ' in product_card or f'"{k.keyword} ' in product_card or f' {k.keyword}"' in product_card or f'{k.keyword} ' in product_card or f' {k.keyword}' in product_card and len(k.keyword) > 1).order_by(lambda: desc(k.requests))[:]
        elif article:
            return select(k for k in KeyWord if int(article) in k.search_1 or int(article) in k.search_2 or int(article) in k.search_3 if k.is_today == is_today)[:]
        else:
            return select([k.id, k.keyword, k.requests] for k in KeyWord if k.is_today == is_today).order_by(lambda: k.id)[:]
    

    @db_session()
    def delete_keywords(self, is_today=None):
        if is_today != None:
            for k in select(k for k in KeyWord if not k.is_today)[:]:
                if KeyWord.exists(keyword=k.keyword, is_today=True):
                    k.delete()
                else:
                    k.is_today = True

    
    """ExportMain requests"""
    @db_session()
    def create_exportmain(self, 
                          employee_id : int,
                          nmId_size : str,
                          nmId : str,
                          size : str,
                          seller_name : str,
                          product_name : str,
                          quantity : int,
                          quantity_till : int,
                          orders_90 : int,
                          orders_30 : int,
                          orders_14 : int,
                          stock_reserve : int,
                          forsupply_14 : int,
                          forsupply_N : int,
                          sales_90 : int,
                          buyout : int,
                          rating : int,
                          updatet_at : datetime,
                          abc_percent : int,
                          abc : str, ):
        employee = User_Seller[employee_id]
        if not ExportMain.exists(employee=employee, nmId=nmId):
            ExportMain(employee=employee,
                       nmId_size=nmId_size,
                       nmId=nmId,
                       size=size,
                       seller_name=seller_name,
                       product_name=product_name,
                       quantity=quantity,
                       quantity_till=quantity_till,
                       orders_90=orders_90,
                       orders_30=orders_30,
                       orders_14=orders_14,
                       stock_reserve=stock_reserve,
                       forsupply_14=forsupply_14,
                       forsupply_N=forsupply_N,
                       sales_90=sales_90,
                       buyout=buyout,
                       rating=rating,
                       updatet_at=updatet_at,
                       abc_percent=abc_percent,
                       abc=abc, )
        else:
            exportmain_to_update = ExportMain.get(employee=employee, nmId=nmId)
            exportmain_to_update.nmId_size=nmId_size
            exportmain_to_update.size=size
            exportmain_to_update.seller_name=seller_name
            exportmain_to_update.product_name=product_name
            exportmain_to_update.quantity=quantity
            exportmain_to_update.quantity_till=quantity_till
            exportmain_to_update.orders_90=orders_90
            exportmain_to_update.orders_30=orders_30
            exportmain_to_update.orders_14=orders_14
            exportmain_to_update.stock_reserve=stock_reserve
            exportmain_to_update.forsupply_14=forsupply_14
            exportmain_to_update.forsupply_N=forsupply_N
            exportmain_to_update.sales_90=sales_90
            exportmain_to_update.buyout=buyout
            exportmain_to_update.rating=rating
            exportmain_to_update.updatet_at=updatet_at
            exportmain_to_update.abc_percent=abc_percent
            exportmain_to_update.abc=abc
    
    
    
    """Commission requests"""
    @db_session()
    async def create_comission(self, category, subject, percent):
        if Comission.exists(subject=subject):
            comission = Comission.get(subject=subject)
            comission.percent = percent
        else:
            comission = Comission(category=category, subject=subject, percent=percent)
        return comission
    
    @db_session()
    def get_comission(self, subject):
        if Comission.exists(subject=subject):
            comission = Comission.get(subject=subject)
            return comission.percent
        else:
            return 19

    