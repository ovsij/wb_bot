from aiogram import F, Router, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.main import bot
from bot.database.database import *
from bot.database.functions.db_requests import DbRequests
from bot.keyboards import *
from bot.utils.states import *
from bot.utils.couponusersfile import *


admin_callbacks_router = Router()

@admin_callbacks_router.callback_query(lambda c: c.data.startswith('admin'))
async def admin_callback_query_handler(callback_query: types.CallbackQuery, state: FSMContext, db_request: DbRequests):
    code = callback_query.data
    tg_id = str(callback_query.from_user.id)
    print('admin: ' + code)
    if code == 'admin_delete_msg':
        await state.clear()
        await callback_query.message.delete()
    if code == 'admin':
        await state.clear()
        text, reply_markup = inline_kb_admin(db_request)
        try:
            await callback_query.message.edit_text(text=text, reply_markup=reply_markup)
        except:
            await callback_query.message.delete()
            await callback_query.message.answer(text=text, reply_markup=reply_markup)
    if 'admin_sending' in code:
        if code == 'admin_sending':
            await state.set_state(Form.sending)
            text, reply_markup = inline_kb_sending()
            msg = await callback_query.message.answer(text=text, reply_markup=reply_markup)
            await state.update_data(message=msg)
        if 'accept' in code:
            data = await state.get_data()
            if 'all' in code:
                users = db_request.get_user()
            elif 'new' in code:
                users = db_request.get_user(date='week')

            for user in users:
                try:
                    await bot.send_message(chat_id=user.tg_id, text=data['text'])
                except:
                    pass

            await callback_query.message.answer(text=data['text'] + '\n\nСообщение отправлено', reply_markup=InlineConstructor.create_kb(text_and_data=[['Скрыть', 'delete_msg']]))
            await callback_query.message.delete()
    if code == 'admin_addadmin':
        await state.set_state(Form.admin)
        await state.update_data(admin_message=callback_query.message)
        text, reply_markup = inline_kb_addadmin()
        msg = await callback_query.message.answer(text=text, reply_markup=reply_markup)
        await state.update_data(message=msg)
    if 'admin_deladmin' in code:
        if len(code.split('_')) == 3:
            u = db_request.update_user(id=int(code.split('_')[-1]), updated_fields={'is_admin' : False})
            print(u)
        text, reply_markup = inline_kb_deladmin(db_request)
        await callback_query.message.edit_text(text=text, reply_markup=reply_markup)
    if 'admin_coupon' in code:
        await state.clear()
        if len(code.split('_')) == 2:
            text, reply_markup = inline_kb_admin_coupon(db_request)
            await callback_query.message.edit_text(text=text, reply_markup=reply_markup)
        else:
            text, reply_markup = inline_kb_admin_coupon(db_request, coupon_id=int(code.split('_')[-1]))
            await callback_query.message.edit_text(text=text, reply_markup=reply_markup)
    if 'admin_delcoupon' in code:
        if 'accept' in code:
            db_request.delete_coupon(id=code.split('_')[-1])
            text, reply_markup = inline_kb_admin_coupon(db_request)
            await callback_query.message.edit_text(text=text, reply_markup=reply_markup)
        else:
            text, reply_markup = inline_kb_delcoupon(db_request, coupon_id=int(code.split('_')[-1]))
            await callback_query.message.edit_text(text=text, reply_markup=reply_markup)
    if code == 'admin_addcoupon':
        await state.set_state(Form.addcoupon)
        text, reply_markup = inline_kb_addcoupon(stage='name')
        msg = await callback_query.message.edit_text(text=text, reply_markup=reply_markup)

        await state.update_data(message=msg)
        await state.update_data(admin_message=callback_query.message)
        await state.update_data(name=None)
    if 'admin_coupusers' in code:
        file = create_file(db_request, coupon_id=code.split('_')[-1])
        text, reply_markup = inline_kb_couponusers(db_request, coupon_id=int(code.split('_')[-1]))
        await callback_query.message.answer_document(types.FSInputFile('users.txt'), reply_markup=reply_markup)

