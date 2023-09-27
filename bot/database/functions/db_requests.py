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
                 coupon_id : int = None, ):
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
    def get_seller(self, id : int = None, user_id : int = None):
        if id:
            return Seller[id]
        if user_id:
            return select(s for s in Seller if User_Seller.get(user=User[user_id]) in s.users)[:]
    
    @db_session()
    def update_seller(self, id : int, 
                      name : str = None, 
                      user_id : int = None,
                      token : str = None,
                      products : list = [],
                      dragon : bool = None, 
                      export : bool = None, 
                      tariff : int = None):
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
        return seller_to_update
    
    @db_session()
    def delete_seller(self, id : int):
        return Seller[id].delete()
    
    @db_session()
    def seller_exists(self, id : int = None):
        if id:
            return Seller.exists(id=id)
    
    @db_session()
    def user_seller_exists(self, user_id : int = None):
        return User_Seller.exists(user=User[user_id])
    
    @db_session()
    def get_employee(self, id : int = None, seller_id : int = None, user_id : int = None):
        if id:
            return User_Seller[id]
        if seller_id and not user_id:
            return select(u for u in User_Seller if u.seller.id == seller_id)[:]
        if user_id:
            return select(u for u in User_Seller if u.seller.id == seller_id and u.user.id == user_id)[:][0]
    
    @db_session()
    def update_employee(self, id : int, 
                        is_orders : bool = None, 
                        is_pay : bool = None, 
                        is_key_words : bool = None, 
                        is_article : bool = None, 
                        stock_reserve : int = None, 
                        order_notif_end : bool = None, 
                        order_notif_ending : bool = None, 
                        order_notif_commission : bool = None, 
                        order_notif_favorites : bool = None, 
                        buyout_notif_end : bool = None, 
                        buyout_notif_ending : bool = None, 
                        buyout_notif_commission : bool = None, 
                        buyout_notif_favorites : bool = None, 
                        cancel_notif : bool = None, ):
        
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
        return employee_to_update
    
    @db_session()
    def delete_employee(self, id : int):
        return User_Seller[id].delete()
    
    """Transaction requests"""
    @db_session()
    def create_transaction(self, user_id : int, sum : int, type : bool, coupon_name : str = None, bill_link : str = None, bill_number : int = None):
        user = User[user_id]
        bill_link_ = f'Купон: {coupon_name}' if coupon_name else bill_link

        transaction = Transaction(user=user, sum=sum, type=type, bill_link=bill_link_)

        if bill_number:
            transaction.bill_number = bill_number
            
        if type:
            user.balance += sum
        else:
            user.balance -= sum


        return user, transaction
        
    @db_session()
    def get_transaction(self, id : int = None, user_id : int = None):
        if id:
            return Transaction[id]
        if user_id:
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