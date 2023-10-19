from aiogram import F, Router, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery


from bot.database.database import *
from bot.database.functions.db_requests import DbRequests
from bot.keyboards import *
from bot.utils.states import *


user_callbacks_router = Router()


@user_callbacks_router.callback_query()
async def user_callback_query_handler(callback_query: types.CallbackQuery, state: FSMContext, db_request: DbRequests):
    code = callback_query.data
    tg_id = str(callback_query.from_user.id)
    print(code)
    if code == 'delete_msg':
        await state.clear()
        await callback_query.message.delete()
    if code == 'start':
        text, reply_markup = inline_kb_start()
        await callback_query.message.edit_text(text=text, reply_markup=reply_markup)
    if code == 'connect':
        await state.set_state(Form.wb_token)
        await state.update_data(stage='connect')
        text, reply_markup = inline_kb_start_connect()
        await callback_query.message.edit_text(text=text, reply_markup=reply_markup)
    if code == 'about_API':
        await state.clear()
        text, reply_markup = inline_kb_about_API()
        await callback_query.message.edit_text(text=text, reply_markup=reply_markup)
    if 'add_employee' in code:
        seller_id = int(code.split('_')[-1])
        text, reply_markup = inline_kb_add_employee(db_request, seller_id=seller_id, tg_id=tg_id)
        await callback_query.message.edit_text(text=text, reply_markup=reply_markup)
    if 'del_employee' in code:
        employee_id = int(code.split('_')[-1])
        seller_id = int(code.split('_')[-2])
        db_request.delete_employee(id=employee_id)
        text, reply_markup = inline_kb_add_employee(db_request, seller_id=seller_id, tg_id=tg_id)
        await callback_query.message.edit_text(text=text, reply_markup=reply_markup)
    if 'employee_link' in code:
        seller_id = int(code.split('_')[-1])
        text, reply_markup = inline_kb_create_employee_link(seller_id=seller_id, tg_id=callback_query.from_user.id)
        await callback_query.message.edit_text(text=text, reply_markup=reply_markup)
    if code == 'my':
        text, reply_markup = inline_kb_my(db_request, tg_id=tg_id)
        try:
            await callback_query.message.edit_text(text=text, reply_markup=reply_markup)
        except:
            await callback_query.message.answer(text=text, reply_markup=reply_markup)
    if 'settings' in code:
        if len(code.split('_')) > 1:
            await state.clear()
            seller_id = int(code.split('_')[-1])
            if 'isorders' in code:
                employee = db_request.get_employee(seller_id=seller_id, user_id=db_request.get_user(tg_id=tg_id).id)
                print(not employee.is_orders)
                db_request.update_employee(id=employee.id, is_orders=not employee.is_orders)
            if 'ispay' in code:
                employee = db_request.get_employee(seller_id=seller_id, user_id=db_request.get_user(tg_id=tg_id).id)
                db_request.update_employee(id=employee.id, is_pay=not employee.is_pay)
            if 'export' in code:
                seller = db_request.get_seller(id=seller_id)
                db_request.update_seller(id=seller.id, export=not seller.export)
            if 'iskeywords' in code:
                employee = db_request.get_employee(seller_id=seller_id, user_id=db_request.get_user(tg_id=tg_id).id)
                db_request.update_employee(id=employee.id, is_key_words=not employee.is_key_words)
            if 'dragon' in code:
                seller = db_request.get_seller(id=seller_id)
                db_request.update_seller(id=seller.id, dragon=not seller.dragon)
            if 'articletype' in code:
                employee = db_request.get_employee(seller_id=seller_id, user_id=db_request.get_user(tg_id=tg_id).id)
                db_request.update_employee(id=employee.id, is_article=not employee.is_article)
            if 'stockreserve' in code:
                await state.set_state(Form.stockreserve)
                await state.update_data(seller_id=seller_id)
                text, reply_markup = inline_kb_stockreserve(db_request, seller_id=seller_id, tg_id=tg_id)
                msg = await callback_query.message.edit_text(text=text, reply_markup=reply_markup)
                await state.update_data(message=msg)
                return
            text, reply_markup = inline_kb_shop_settings(db_request, seller_id=seller_id, tg_id=tg_id)
            await callback_query.message.edit_text(text=text, reply_markup=reply_markup)
            return
        if len(db_request.get_seller(user_id=db_request.get_user(tg_id=tg_id).id)) > 0:
            text, reply_markup = inline_kb_settings(db_request, tg_id=tg_id)
            await state.clear()
        else:
            text, reply_markup = inline_kb_start()
        await callback_query.message.edit_text(text=text, reply_markup=reply_markup)
    if code == 'add_seller':
        await state.set_state(Form.wb_token)
        await state.update_data(stage='add_seller')
        text, reply_markup = inline_kb_add_seller()
        await callback_query.message.edit_text(text=text, reply_markup=reply_markup)
    if 'apifbo' in code:
        if 'changeapifbo' in code:
            await state.set_state(Form.wb_token)
            await state.update_data(stage='changeapifbo', seller_id=int(code.split('_')[-1]))
            text, reply_markup = inline_kb_change_apifbo(db_request, seller_id=int(code.split('_')[-1]))
            await callback_query.message.edit_text(text=text, reply_markup=reply_markup)
        if 'delapifbo' in code:
            if 'accept' in code:
                db_request.delete_employee(id=code.split('_')[-1])
                text, reply_markup = inline_kb_settings(db_request, tg_id=tg_id)
            else:
                text, reply_markup = inline_kb_del_apifbo(db_request, seller_id=int(code.split('_')[-2]), employee_id=int(code.split('_')[-1]), tg_id=tg_id)
            await callback_query.message.edit_text(text=text, reply_markup=reply_markup)
        else:
            text, reply_markup = inline_kb_apifbo(db_request, seller_id=int(code.split('_')[-1]), tg_id=tg_id)
            await callback_query.message.edit_text(text=text, reply_markup=reply_markup)
    if 'apifbs' in code:
        await state.set_state(Form.wb_token)
        await state.update_data(stage='add_apifbs', seller_id=int(code.split('_')[-1]))
        text, reply_markup = inline_kb_apifbs(db_request, seller_id=int(code.split('_')[-1]))
        await callback_query.message.edit_text(text=text, reply_markup=reply_markup)
    if 'notifications' in code:
        text, reply_markup = inline_kb_notifications(db_request, seller_id=int(code.split('_')[-1]))
        await callback_query.message.edit_text(text=text, reply_markup=reply_markup)
    if 'notiforders' in code:
        seller_id = int(code.split('_')[-2]) if len(code.split('_')) == 3 else int(code.split('_')[-3]) if 'all' in code else int(code.split('_')[-1])
        employee = db_request.get_employee(seller_id=seller_id, user_id=db_request.get_user(tg_id=tg_id).id)
        button = code.split('_')[-1] if len(code.split('_')) > 2 else 'nothing'
        
        if button == 'all':
            db_request.update_employee(id=employee.id,
                                    order_notif_end=True,
                                    order_notif_ending=True,
                                    order_notif_commission=True,
                                    order_notif_favorites=True
                                    )

        if button == 'none':
            db_request.update_employee(id=employee.id,
                                    order_notif_end=False,
                                    order_notif_ending=False,
                                    order_notif_commission=False,
                                    order_notif_favorites=False
                                    )
            
        if button == '1':
            if code.split('_')[-2] == 'all':
                db_request.update_employee(id=employee.id,
                                           order_notif_end=True,
                                           order_notif_ending=False,
                                           order_notif_commission=False,
                                           order_notif_favorites=False)
            else:
                db_request.update_employee(id=employee.id,
                                           order_notif_end=not employee.order_notif_end)
        if button == '2':
            if code.split('_')[-2] == 'all':
                db_request.update_employee(id=employee.id,
                                           order_notif_end=False,
                                           order_notif_ending=True,
                                           order_notif_commission=False,
                                           order_notif_favorites=False)
            else:
                db_request.update_employee(id=employee.id,
                                           order_notif_ending=not employee.order_notif_ending)
        if button == '3':
            if code.split('_')[-2] == 'all':
                db_request.update_employee(id=employee.id,
                                           order_notif_end=False,
                                           order_notif_ending=False,
                                           order_notif_commission=True,
                                           order_notif_favorites=False)
            else:
                db_request.update_employee(id=employee.id,
                                           order_notif_commission=not employee.order_notif_commission)
        if button == '4':
            if code.split('_')[-2] == 'all':
                db_request.update_employee(id=employee.id,
                                           order_notif_end=False,
                                           order_notif_ending=False,
                                           order_notif_commission=False,
                                           order_notif_favorites=True)
            else:
                db_request.update_employee(id=employee.id,
                                           order_notif_favorites=not employee.order_notif_favorites)
            
        button = code.split('_')[-1] if len(code.split('_')) > 2 else 'all' if len(code.split('_')) == 2 else 'nothing'
        text, reply_markup = inline_kb_notiforders(db_request, employee_id=employee.id, seller_id=seller_id, button=button)
        await callback_query.message.edit_text(text=text, reply_markup=reply_markup)
    if 'notifbuyout' in code:
        seller_id = int(code.split('_')[-2]) if len(code.split('_')) == 3 else int(code.split('_')[-1])
        employee = db_request.get_employee(seller_id=seller_id, user_id=db_request.get_user(tg_id=tg_id).id)
        button = code.split('_')[-1] if len(code.split('_')) == 3 else 'no changing'
        if button == 'all':
            db_request.update_employee(id=employee.id,
                                       buyout_notif_end=True,
                                       buyout_notif_ending=True,
                                       buyout_notif_commission=True,
                                       buyout_notif_favorites=True
                                       )
        if button == 'none':
            db_request.update_employee(id=employee.id,
                                       buyout_notif_end=False,
                                       buyout_notif_ending=False,
                                       buyout_notif_commission=False,
                                       buyout_notif_favorites=False
                                       )
        if button == '1':
            if code.split('_')[-2] == 'all':
                db_request.update_employee(id=employee.id,
                                        buyout_notif_end=True,
                                        buyout_notif_ending=False,
                                        buyout_notif_commission=False,
                                        buyout_notif_favorites=False)
            else:
                db_request.update_employee(id=employee.id,
                                        buyout_notif_end=not employee.buyout_notif_end)
                
        if button == '2':
            if code.split('_')[-2] == 'all':
                db_request.update_employee(id=employee.id,
                                        buyout_notif_end=False,
                                        buyout_notif_ending=True,
                                        buyout_notif_commission=False,
                                        buyout_notif_favorites=False)
            else:
                db_request.update_employee(id=employee.id,
                                       buyout_notif_ending=not employee.buyout_notif_ending)
        if button == '3':
            if code.split('_')[-2] == 'all':
                db_request.update_employee(id=employee.id,
                                        buyout_notif_end=False,
                                        buyout_notif_ending=False,
                                        buyout_notif_commission=True,
                                        buyout_notif_favorites=False)
            else:
                db_request.update_employee(id=employee.id,
                                       buyout_notif_commission=not employee.buyout_notif_commission)
        if button == '4':
            if code.split('_')[-2] == 'all':
                db_request.update_employee(id=employee.id,
                                        buyout_notif_end=False,
                                        buyout_notif_ending=False,
                                        buyout_notif_commission=False,
                                        buyout_notif_favorites=True)
            else:
                db_request.update_employee(id=employee.id,
                                       buyout_notif_favorites=not employee.buyout_notif_favorites)
        button = code.split('_')[-1] if len(code.split('_')) > 2 else 'all' if len(code.split('_')) == 2 else 'nothing'
        text, reply_markup = inline_kb_notifbuyout(db_request, employee_id=employee.id, seller_id=seller_id, button=button)
        await callback_query.message.edit_text(text=text, reply_markup=reply_markup)
    if 'notifcancel' in code:
        seller_id = int(code.split('_')[-2]) if len(code.split('_')) > 2 else int(code.split('_')[-1])
        employee = db_request.get_employee(seller_id=seller_id, user_id=db_request.get_user(tg_id=tg_id).id)
        if len(code.split('_')) > 2:
            if code.split('_')[-1] == '1':
                db_request.update_employee(id=employee.id,
                                        cancel_notif=True)
            else:
                db_request.update_employee(id=employee.id,
                                        cancel_notif=False)
        text, reply_markup = inline_kb_notifcancel(db_request, seller_id=seller_id, employee_id=employee.id)
        await callback_query.message.edit_text(text=text, reply_markup=reply_markup)
    if code == 'balanсe':
        await state.clear()
        text, reply_markup = inline_kb_balance(db_request, tg_id=tg_id)
        await callback_query.message.edit_text(text=text, reply_markup=reply_markup)
    if 'transaction' in code:
        sum = code.split('_')[-1]
        # TODO
        # добавить создание платежной ссылки
        #
        payment_link = ''
        text, reply_markup = inline_kb_payment(sum, payment_link)
        await callback_query.message.edit_text(text=text, reply_markup=reply_markup)
    if code == 'credit':
        text, reply_markup = inline_kb_credit(db_request, tg_id=tg_id)
        await callback_query.message.edit_text(text=text, reply_markup=reply_markup)
    if code == 'debit':
        text, reply_markup = inline_kb_debit(db_request, tg_id=tg_id)
        await callback_query.message.edit_text(text=text, reply_markup=reply_markup)
    if code == 'coupon':
        await state.set_state(Form.addusercoupon)
        text, reply_markup = inline_kb_coupon()
        msg = await callback_query.message.edit_text(text=text, reply_markup=reply_markup)
        await state.update_data(message=msg)
    if 'news' in code:
        if 'add' in code:
            text, reply_markup = inline_kb_addnews(code.split('_')[-1])
            await state.set_state(Form.addnews)
        elif 'del' in code:
            db_request.delete_news(id=int(code.split('_')[-1]))
            news_id = None if code.split('_')[-2] == 'None' else int(code.split('_')[-2])
            text, reply_markup = inline_kb_news(db_request, news_id=news_id, tg_id=tg_id)
        else:
            news_id = int(code.split('_')[-1])
            text, reply_markup = inline_kb_news(db_request, news_id=news_id, tg_id=tg_id)
        await callback_query.message.edit_text(text=text, reply_markup=reply_markup)
    if code == 'stock':
        text, reply_markup = inline_kb_stocks(db_request, tg_id=tg_id)
        await callback_query.message.edit_text(text=text, reply_markup=reply_markup)
    if 'selectseller' in code:
        if len(code.split('_')) > 2:
            user = db_request.get_user(tg_id=tg_id)
            if 'all' in code:
                for seller in db_request.get_seller(user_id=user.id):
                    employee = db_request.get_employee(seller_id=seller.id, user_id=user.id)
                    db_request.update_employee(id=employee.id, is_selected=True)
            else:
                seller_id = int(code.split('_')[-1])
                employee = db_request.get_employee(seller_id=seller_id, user_id=user.id)
                if all([e.is_selected for e in db_request.get_employee(user_id=user.id)]) and '👉' in callback_query.message.reply_markup.inline_keyboard[-2][0].text:
                    for seller in db_request.get_seller(user_id=user.id):
                        employee_ = db_request.get_employee(seller_id=seller.id, user_id=user.id)
                        db_request.update_employee(id=employee_.id, is_selected=False)
                    db_request.update_employee(id=employee.id, is_selected=True)
                else:
                    db_request.update_employee(id=employee.id, is_selected=not employee.is_selected)
                if not any(e.is_selected for e in db_request.get_employee(user_id=user.id)):
                    for seller in db_request.get_seller(user_id=user.id):
                        employee_ = db_request.get_employee(seller_id=seller.id, user_id=user.id)
                        db_request.update_employee(id=employee_.id, is_selected=True)
        if 'stock' in code:
            btn_back = 'stock'
        elif 'reports' in code:
            btn_back = 'reports'
        code = code.split('_')[-1] if len(code.split('_')) > 2 else 'all'
        text, reply_markup = inline_kb_selectseller(db_request, tg_id=tg_id, code=code, back=btn_back)
        await callback_query.message.edit_text(text=text, reply_markup=reply_markup)
    if 'myproducts' in code or 'favorites' in code or 'archive' in code:
        if len(code.split('_')) > 2:
            db_request.update_user(tg_id=tg_id, updated_fields={'stock_sorting': StockSorting.from_str(code.split('_')[1])})

        text, reply_markup = inline_kb_stock_myproducts(db_request, tg_id=tg_id, page=int(code.split('_')[-1]), filter=code.split('_')[0])
        msg = await callback_query.message.edit_text(text=text, reply_markup=reply_markup)
        await state.set_state(Form.my_products)
        await state.update_data(page=int(code.split('_')[-1]))
        await state.update_data(msg_to_edit=msg)
        await state.update_data(filter=code.split('_')[0])   
    if 'addfav' in code or 'delfav' in code:
        user = db_request.get_user(tg_id=tg_id)
        for id in code.replace('addfav_', '').replace('delfav_', '').split('_'):
            product = db_request.get_product(id=int(id))
            employee = db_request.get_employee(seller_id=product.seller.id, user_id=user.id)
            db_request.update_employee(id=employee.id, favorites=product.id)
        data = await state.get_data()
        text, reply_markup = inline_kb_stock_myproducts(db_request, tg_id=tg_id, page=data['page'], filter=data['filter'])
        await callback_query.message.edit_text(text=text, reply_markup=reply_markup)     

    if 'reports' in code:
        if 'deny' in code:
            await state.clear()
            search = None
        else:
            data = await state.get_data()
            try:
                search = data['search']
            except:
                search = None

        if len(code.split('_')) > 3:
            db_request.update_user(tg_id=tg_id, updated_fields={'reports_groupby': ReportsGroupBy.from_str(code.split('_')[-3])})
        
        if code == 'reports':
            text, reply_markup = inline_kb_reports(db_request, tg_id=tg_id)
            await callback_query.message.edit_text(text=text, reply_markup=reply_markup)
        elif code == 'reports_timedelta':
            text, reply_markup = inline_kb_reports_timedelta()
            msg = await callback_query.message.answer(text=text, reply_markup=reply_markup)
            await state.set_state(Form.reports_timedelta)
            await state.update_data(msg_for_edit=callback_query.message)
            await state.update_data(msg_for_delete=msg)
        else:
            text, reply_markup = inline_kb_reports_byperiod(db_request, state, tg_id=tg_id, period=code.split('_')[-2], page=int(code.split('_')[-1]), search=search)
            await callback_query.message.edit_text(text=text, reply_markup=reply_markup)
    if 'reportorders' in code:
        if 'deny' in code:
            await state.clear()
            search = None
        else:
            data = await state.get_data()
            try:
                search = data['search']
            except:
                search = None
        if code.split('_')[-2] in ['days', 'weeks', 'months', 'withoutgroup']:
            db_request.update_user(tg_id=tg_id, updated_fields={'reports_groupby_period': ReportsGroupByPeriod.from_str(code.split('_')[-2])})
        text, reply_markup = inline_kb_orders(db_request, tg_id=tg_id, page=int(code.split('_')[-1]), search=search)
        await callback_query.message.edit_text(text=text, reply_markup=reply_markup)
    if 'repsales' in code:
        if 'deny' in code:
            await state.clear()
            search = None
        else:
            data = await state.get_data()
            try:
                search = data['search']
            except:
                search = None
        if code.split('_')[-2] in ['days', 'weeks', 'months', 'withoutgroup']:
            db_request.update_user(tg_id=tg_id, updated_fields={'reports_groupby_period': ReportsGroupByPeriod.from_str(code.split('_')[-2])})
        type = 'S' if 'S' in code else 'R' if 'R' in code else 'D'
        text, reply_markup = inline_kb_sales(db_request, tg_id=tg_id, page=int(code.split('_')[-1]), search=search, type=type)
        await callback_query.message.edit_text(text=text, reply_markup=reply_markup)

    if 'search' in code:
        await state.set_state(Form.search)
        await state.update_data(type=code.split('_')[-1])
        if 'report' in code:
            await state.update_data(period=code.split('_')[-2])
        text, reply_markup = inline_kb_search()
        msg = await callback_query.message.answer(text=text, reply_markup=reply_markup)
        await state.update_data(msg_to_delete=msg)
        await state.update_data(msg_to_edit=callback_query.message)

            
