from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    wb_token = State()
    stockreserve = State()
    sending = State()
    admin = State()
    addcoupon = State()
    addusercoupon = State()
    addnews = State()
