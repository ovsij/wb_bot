from datetime import datetime, timedelta

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.formatting import *
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.config import load_config
from bot.keyboards import InlineConstructor, btn_back

config = load_config('.env')

def inline_kb_admin(db_request):
    text = as_line(Bold('🦸🏻‍♂️ Кабинет администратора'),
                   '',
                   'Администраторы:',
                   '',
                   sep='\n'
    )
    for user in db_request.get_user(is_admin=True):
        user = db_request.get_user(id=user.id)
        last_name = user.last_name if user.last_name else ''
        first_name = user.first_name if user.first_name else ''
        text += as_line(TextLink(f'{first_name} {last_name} @{user.username}\n', url=f't.me/{user.username}'))
    
    text_and_data = [
        ['Рассылка', 'admin_sending'],
        ['Добавить админа', 'admin_addadmin'],
        ['Удалить админа', 'admin_deladmin'],
        ['Купоны', 'admin_coupon'],
    ]
    reply_markup = InlineConstructor.create_kb(text_and_data)
    return text.as_html(), reply_markup

def inline_kb_sending():
    text = 'Пришлите текст сообщения для рассылки:'
    reply_markup = InlineConstructor.create_kb([btn_back('admin_delete_msg')])
    return text, reply_markup

def inline_kb_addadmin():
    text = 'Пришлите username пользователя, которого вы хотите сделать администратором (без @). Например: Kilovatts'
    reply_markup = InlineConstructor.create_kb([btn_back('admin_delete_msg')])
    return text, reply_markup

def inline_kb_deladmin(db_request):
    admins = db_request.get_user(is_admin=True)
    text = 'Выберите админа, которого вы хотите удалить'
    text_and_data = []
    for admin in admins:
        if int(admin.tg_id) not in config.bot.admin_ids:
            text_and_data.append([admin.username, f'admin_deladmin_{admin.id}'])
    text_and_data.append(btn_back('admin'))
    reply_markup = InlineConstructor.create_kb(text_and_data=text_and_data)
    return text, reply_markup

def inline_kb_admin_coupon(db_request, coupon_id : int = None):
    if coupon_id:
        coupon = db_request.get_coupon(id=coupon_id)
        users = db_request.get_user(coupon_id=coupon.id)
        text = as_line(Bold(f'Купон: {coupon.name}'),
                       '',
                       f'Сумма: {coupon.sum}',
                       '',
                       f'Пользователи: {len(users)}',
                       sep='\n'
                       )
        text_and_data = [
            ['Удалить купон', f'admin_delcoupon_{coupon.id}'],
            ['Пользователи', f'admin_coupusers_{coupon.id}'],
            btn_back('admin_coupon')
        ]
        reply_markup = InlineConstructor.create_kb(text_and_data=text_and_data)
        return text.as_html(), reply_markup
    else:
        coupones = db_request.get_coupon()
        text = 'Купоны'
        text_and_data = []
        for coupon in coupones:
            text_and_data.append([f'{coupon.name} | {coupon.sum}р', f'admin_coupon_{coupon.id}'])
        text_and_data.append(['+ Добавить купон', 'admin_addcoupon'])
        text_and_data.append(btn_back('admin'))
        reply_markup = InlineConstructor.create_kb(text_and_data=text_and_data)
        return text, reply_markup
    
def inline_kb_delcoupon(db_request, coupon_id : int):
    coupon = db_request.get_coupon(id=coupon_id)
    text = as_line(f'Купон: {coupon.name}',
                   '',
                   'При удалении купона будет удалена вся информация о статистике его использования.',
                   '',
                   'Вы уверены, что хотите продолжить?',
                   sep='\n'
                   )
    text_and_data = [
        ['Удалить купон', f'admin_delcoupon_accept_{coupon.id}'],
        btn_back(f'admin_coupon_{coupon.id}')
    ]
    reply_markup = InlineConstructor.create_kb(text_and_data=text_and_data)
    return text.as_html(), reply_markup

def inline_kb_addcoupon(stage : str):
    if stage == 'name':
        text = 'Введите название купона, который вы хотите создать:'
    else:
        text = 'Введите сумму купона в рублях:'
    reply_markup = InlineConstructor.create_kb(text_and_data=[btn_back('admin_coupon')])
    return text, reply_markup

def inline_kb_couponusers(db_request, coupon_id : int):
    coupon = db_request.get_coupon(id=coupon_id)
    text = 'Информация о пользователях в прикрепленном файле'
    reply_markup = InlineConstructor.create_kb(text_and_data=[['Скрыть', 'admin_delete_msg']])
    return text, reply_markup