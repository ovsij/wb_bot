from datetime import date, datetime, timedelta

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.formatting import *
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.config import load_config
from bot.database.enum import *
from bot.keyboards import InlineConstructor, btn_back

config = load_config('.env')

def inline_kb_start():
    text = as_line('🤜🏻 {bot_name} - это незаменимый помощник, который позволяет просто и эффективно контролировать продажи на Wildberries. ',
                   '',
                   Bold('БОТ ПОКАЖЕТ:  '),
                   '',
                   '🛒 Уведомления о новых заказах;',
                   '✅ Уведомления о выкупах;',
                   '↩ Уведомления о возвратах;',
                   '💼 Фактическую комиссию по заказу;',
                   '💎 Процент выкупа по текущему артикулу;',
                   '🌐 Регион покупателя и стоимость логистики;',
                   '📦 Реальные остатки на складе и на сколько дней хватит резерва;',
                   '🚗 Сообщит о необходимости новой поставки;',
                   '🔍 Позиции по ключевым фразам в выдаче.',
                   '',
                   Bold('ОСОБЕННОСТИ:'),
                   '',
                   '🐉 Работа во время сбоев, когда серверы WB не отвечают, а другие боты нервно молчат;',
                   '📊 Построение информативных отчетов по заказам, продажам, возвратам и штрафам;',
                   '↔️ Возможность подключения нескольких кабинетов Wildberries;',
                   '📑 Выгрузка данных в Google таблицы с обновлением в реальном времени;',
                   '🔕 Отсутствие рекламных рассылок и лишних уведомлений;',
                   '👨🏻‍💻 Оперативная и доброжелательная техподдержка.',
                   '',
                   Bold('НЕ НАРУШАЕТ ОФЕРТУ WB:'),
                   '',
                   '✅ Для работы используется официальный публичный сервер статистики https://openapi.wb.ru.',
                   '🛡 Пользование ботом абсолютно безопасно.',
                   '',
                   '🔥 Теперь вся горячая информация о продажах на экране вашего смартфона!',
                   sep='\n'
    )
    text_and_data = [
        ['👉 Подключить бесплатно', 'connect'],
    ]
    keyboard = InlineConstructor.create_kb(text_and_data)
    return text.as_html(), keyboard

def inline_kb_start_connect():
    text = as_line(Bold('🛠 ПОДКЛЮЧЕНИЕ'), 
                       '',
                       '☑️Подключаясь к боту, вы принимаете нашу оферту.',
                       '',
                       '1️⃣ Зайдите в Личный кабинет WB → Настройки → Доступ к API (ссылка).',
                       '2️⃣ Нажмите кнопку [Создать новый токен]. Введите любое имя токена (например {bot name}) и выберите тип Статистика.',
                       '3️⃣ Нажмите [Создать токен], а затем скопируйте его.',
                       '',
                       '📝 Вставьте скопированный токен в сообщение этого чата:' ,
                       sep='\n')
    
    text_and_data = [
        ['🔍 Подробнее про API', 'about_API'],
        ['🤵 Поддержка', config.bot.support_url]
    ]
    button_type = ['callback_data', 'url']
    keyboard = InlineConstructor.create_kb(text_and_data=text_and_data, button_type=button_type)
    return text.as_html(), keyboard

def inline_kb_about_API():
    text = as_line(Bold('🔑 API токен (ключ) Wildberries'),
                   'Если кратко, то API-токен — это идентификатор поставщика Wildberries, с помощью которого можно получать информацию о заказах, продажах, поступлениях, наличию на складах и другим данным конкретного поставщика, без доступа к личному кабинету. Далее на основе полученной информации можно строить аналитику.', 
                   '',
                   'API-токен — это способ интегрирования с теми или иными сервисами (в том числе {botname}), которые созданы для того, чтобы помочь поставщикам в работе с Wildberries. ',
                   '',
                   Bold('Преимущества API:'),
                   '✴️ С помощью API вы получаете детализированную информацию по продажам, заказам и поставкам. WB же в большинстве своих отчетов даёт лишь общую информацию. ',
                   '✴️ API безопасен и даёт возможность только получать данные, это значит, что вероятность изменения или какого-либо влияния на информацию исключена. ',
                   '✴️ Вы в любой момент можете сгенерировать новый API-токен в личном кабинете WB, а значит отменить доступ к статистическим данным для нашего бота или других сервисов.',
                   sep='\n')
    
    reply_markup = InlineConstructor.create_kb([btn_back('connect')])
    return text.as_html(), reply_markup

def inline_kb_sucсess_start(seller_id : int):
    text = as_line(Bold('✅ Поздравляем, успешное подключение!'),
                   '',
                   '{bot name} теперь работает на вас 🤜🏻',
                   '',
                   '⏳ Как только на WB появится новый заказ, бот соберет необходимую статистику и пришлет уведомление.',
                   '',
                   'С этого момента начнется тестовый период, который продлится 1 сутки',
                   '',
                   '🚙 Если вы работаете по схеме FBS (продажа со склада поставщика), подключите дополнительный API токен (тип стандартный), чтобы бот мог оперативно отслеживать новые FBS заказы.',
                   '',
                   '🔔 Подпишитесь на наш канал, чтобы быть в курсе событий, новых функций и возможностей бота.',
                   sep='\n'
                   )
    text_and_data = [
        ['Подключить FBS API токен', 'add_fbs_api'],
        ['➕ Добавить сотрудника', f'add_employee_{seller_id}'],
    ]
    reply_markup = InlineConstructor.create_kb(text_and_data)
    return text.as_html(), reply_markup

def inline_kb_unsucсess_start():
    text = as_line(Bold('👤 Добавление продавца'),
                   '',
                   '❌Ошибка! API токен некорректен!',
                   '',
                   'При создании укажите тип Статистика. Отправьте правильный токен в сообщении этого чата:',
                   sep='\n'
                   )
    text_and_data = [
        btn_back('settings'),
        ['🤵 Поддержка', config.bot.support_url]
    ]
    schema = [2]
    button_type = ['callback_data', 'url']
    reply_markup = InlineConstructor.create_kb(text_and_data=text_and_data, schema=schema, button_type=button_type)
    return text.as_html(), reply_markup
                   
def inline_kb_add_employee(db_request, seller_id : int, tg_id : str):
    text_and_data = []
    employees = db_request.get_employee(seller_id=seller_id)
    employees_list = []
    current_user = db_request.get_employee(seller_id=seller_id, user_id=db_request.get_user(tg_id=tg_id).id)
    c = 1
    for employee in employees:
        is_admin = '(🦸🏻‍♂️ суперадмин)' if employee.is_admin else ''
        user = db_request.get_user(id=employee.user.id)
        username = db_request.get_user(id=employee.user.id).username
        employee_tg_id = user.tg_id
        e_name = as_line(TextLink(f'{c}. {username} {is_admin}', url=f't.me/{username}')) if \
            username else as_line(TextLink(f'{c}. {employee_tg_id} {is_admin}', url=f'tg://user?id={employee_tg_id}'))
        employees_list.append(e_name)
        c += 1
        if not employee.is_admin and current_user.is_admin:
            name = user.username if user.username else user.tg_id
            text_and_data.append([f'Удалить {name}', f'del_employee_{seller_id}_{employee.id}'])

    text = as_line(Bold(f'🧑🏻‍💼 Сотрудники {len(employees)}'),
                   '', )
    for name in employees_list:
        text += name
    text2 = as_line('',
             'ℹ️ Только суперадмин может добавлять и удалять сотрудников.',
             sep='\n')
    text += text2
    if current_user.is_admin:
        text_and_data += [['➕ Добавить сотрудника', f'employee_link_{seller_id}']]
    text_and_data += [btn_back(f'settings_{seller_id}')]
    
    reply_markup = InlineConstructor.create_kb(text_and_data)
    return text.as_html(), reply_markup

def inline_kb_create_employee_link(seller_id : int, tg_id : int):
    text = as_line(Bold(f'🧑🏻‍💼 Добавление сотрудника'),
                   '',
                   '1️⃣ Отправьте эту ссылку вашему сотруднику:',
                   '',
                   f'{config.bot.bot_url}?start=addemployee_{tg_id}_{seller_id}',
                   '',
                   '2️⃣ Сотруднику необходимо пройти по этой ссылке в бот и нажать на кнопку [Запустить] (на кнопке может быть надпись "Старт" или "Начать").', 
                   sep='\n')
    reply_markup = InlineConstructor.create_kb([btn_back(f'add_employee_{seller_id}')])
    return text.as_html(), reply_markup

def inline_kb_my(db_request, tg_id : str):
    sellers = db_request.get_seller(user_id=db_request.get_user(tg_id=tg_id).id)
    text = as_line(Bold(f'🐲 Личный кабинет'), 
                   '',
                   f'· ID: {tg_id}',
                   '',
                   f'· Поставщики: {len(sellers)}',
                   sep='\n')
    text_and_data = [
        ['⚙️ Настройки', 'settings'],
        ['💰 Баланс', 'balanсe'],
        ['🤵 Поддержка', config.bot.support_url],
        ['📄 Оферта', config.bot.oferta],
    ]
    schema = [2, 1, 1]
    button_type = ['callback_data', 'url', 'url']
    reply_markup = InlineConstructor.create_kb(text_and_data=text_and_data, schema=schema, button_type=button_type)
    return text.as_html(), reply_markup

def inline_kb_settings(db_request, tg_id : str):
    text = '📝 Выберите продавца для редактирования:'
    text_and_data = []
    sellers = db_request.get_seller(user_id=db_request.get_user(tg_id=tg_id).id)
    for seller in sellers:
        text_and_data.append([seller.name, f'settings_{seller.id}'])
    text_and_data.append(['➕ Добавить продавца', 'add_seller'])
    text_and_data.append(btn_back('my'))
    reply_markup = InlineConstructor.create_kb(text_and_data=text_and_data)
    return text, reply_markup

def inline_kb_add_seller():
    text = as_line(Bold(f'👤 Добавление продавца '),
                   '',
                   '↔️ Чтобы отслеживать заказы сразу для нескольких кабинетов WB, добавьте еще один API токен.',
                   '',
                   '1️⃣ Зайдите в Личный кабинет WB → Настройки → Доступ к API (ссылка). ',
                   '',
                   '2️⃣ Нажмите кнопку [Создать новый токен]. Введите любое имя ключа (например WbNinjaBot) и выберите тип Статистика.',
                   '',
                   '3️⃣ Нажмите [Создать токен], а затем скопируйте его.',
                   '',
                   '📝 Вставьте скопированный токен в сообщение этого чата:',
                   sep='\n')
    
    reply_markup = InlineKeyboardBuilder()
    reply_markup.add(InlineKeyboardButton(text='⬅️ Назад', callback_data='settings'))
    reply_markup.add(InlineKeyboardButton(text='🤵 Поддержка', url=config.bot.support_url))
    return text.as_html(), reply_markup.as_markup()

def inline_kb_shop_settings(db_request, seller_id : int, tg_id : str):
    seller = db_request.get_seller(id=seller_id)
    employee = db_request.get_employee(seller_id=seller_id, user_id=db_request.get_user(tg_id=tg_id).id)
    tariff_date = (datetime.now().replace(day=1) + timedelta(days=32)).replace(day=1).strftime('%d.%m.%Y')
    is_orders = ['✅ 🛒 Заказы отслеживаются', '✅ Бот включен'] if employee.is_orders else ['⭕️ 🛒 Заказы не отслеживаются', '⭕️ Бот выключен']
    is_pay = ['✅ 👤 Вы администратор (вы оплачиваете тариф для текущего кабинета)', '✅ Я администратор'] if employee.is_pay else ['⭕️ 👤 Вы пользователь (вы не оплачиваете тариф для текущего кабинета)', '⭕️ Я пользователь']
    export = ['✅ 📑 Экспорт в Google-таблицы включен (подробнее 👉🏻 /export)', '✅ Экспорт в Google-таблицы']  if seller.export else ['⭕️ 📑 Экспорт в Google-таблицы выключен (подробнее 👉🏻 /export)', '⭕️ Экспорт в Google (включить?)']
    is_key_words = ['✅ 🔍 Показ ключевых слов в уведомлениях заказов включен', '✅ Показ ключевых слов']  if employee.is_key_words else ['⭕️ 🔍 Показ ключевых слов в уведомлениях заказов выключен', '⭕️ Показ ключ.слов (включить?)']
    dragon = ['✅ 🐉 Режим «Дракон» включен (подробнее 👉🏻 /dragon)', '✅ Режим «Дракон»']  if seller.dragon else ['⭕️ 🐉 Режим "Дракон" выключен (подробнее 👉🏻 /dragon)', '⭕️ Режим «Дракон» (включить?)']
    
    text = as_line(Bold(f'🥝 {seller.name}'),
                   f'💰 Тариф: {seller.tariff}₽ / мес',
                   f'⏱ Расчёт тарифа: {tariff_date}',
                   '.....',
                   '',
                   is_orders[0],
                   '',
                   is_pay[0],
                   '',
                   export[0],
                   '',
                   is_key_words[0],
                   '',
                   dragon[0],
                   sep='\n'
    )
    article_type = '🆔 Артикул ссылкой' if employee.is_article else '🆔 Артикул текстом + ссылка'
    text_and_data = []
    text_and_data.append([is_orders[1], f'settings_isorders_{seller_id}'])
    text_and_data.append([is_pay[1], f'settings_ispay_{seller_id}'])
    text_and_data.append([export[1], f'settings_export_{seller_id}'])
    text_and_data.append([is_key_words[1], f'settings_iskeywords_{seller_id}'])
    text_and_data.append([dragon[1], f'settings_dragon_{seller_id}'])
    text_and_data.append([article_type, f'settings_articletype_{seller_id}'])
    text_and_data.append([f'📦 Резерв склада {employee.stock_reserve} дн', f'settings_stockreserve_{seller_id}'])
    text_and_data.append(['🔑 API токен FBO (статистика)', f'apifbo_{seller_id}'])
    text_and_data.append(['🔑 API токен FBS (стандартный)', f'apifbs_{seller_id}'])
    text_and_data.append(['🧑‍💼 Сотрудники', f'add_employee_{seller_id}'])
    text_and_data.append(['🔔 Уведомления', f'notifications_{seller_id}'])
    text_and_data.append(['❌ Удалить поставщика', f'delapifbo_{seller_id}_{employee.id}'])
    text_and_data.append(btn_back('settings'))
    reply_markup = InlineConstructor.create_kb(text_and_data=text_and_data)
    return text.as_html(), reply_markup

def inline_kb_stockreserve(db_request, seller_id : int, tg_id : str):
    employee = db_request.get_employee(seller_id=seller_id, user_id=db_request.get_user(tg_id=tg_id).id)
    text = as_line(Bold('📦 Резерв склада '),
                   '',
                   '{bot_name} покажет оптимальное количество товара для новой поставки, просто укажите на сколько дней вы планируете заполнять склад (на сколько дней должно хватать товара при текущей динамике продаж).',
                   '',
                   f'Текущее значение: {employee.stock_reserve} дн.',
                   '',
                   '📝 Введите новое значение в этом сообщении (от 3 до 60):',
                   sep='\n'
    )
    reply_markup = InlineConstructor.create_kb(text_and_data=[btn_back(f'settings_{seller_id}')])
    return text.as_html(), reply_markup

def inline_kb_apifbo(db_request, seller_id : int, tg_id : str):
    seller = db_request.get_seller(id=seller_id)
    employee = db_request.get_employee(seller_id=seller_id, user_id=db_request.get_user(tg_id=tg_id).id)
    text = as_line(Bold('🔑 Управление токеном'),
                   '',
                   f'🥝 {seller.name}',
                   '',
                   '👇🏻 Выберите действие:',
                   sep='\n'
    )
    text_and_data = [
        ['Заменить API токен FBO (статистика)', f'changeapifbo_{seller_id}'],
        ['Удалить API токен FBO (статистика)', f'delapifbo_{seller_id}_{employee.id}'],
        btn_back(f'settings_{seller_id}')
    ]
    reply_markup = InlineConstructor.create_kb(text_and_data=text_and_data)
    return text.as_html(), reply_markup

def inline_kb_change_apifbo(db_request, seller_id : int):
    seller = db_request.get_seller(id=seller_id)
    text = as_line(Bold('🔄 Замена API токена FBO (статистика)'),
                   '',
                   f'🥝 {seller.name}',
                   '',
                   'Замена требуется, если API токен FBO (статистика) был удалён в кабинете Wildberries или вы переходите со старого типа ключа на новый. ',
                   '',
                   '1️⃣ Зайдите в Личный кабинет WB → Настройки → Доступ к API (ссылка). ',
                   '',
                   '2️⃣ Нажмите кнопку [Создать новый токен]. Введите любое имя токена (например {bot_name}}) и выберите тип Статистика.',
                   '',
                   '3️⃣ Нажмите [Создать токен], а затем скопируйте его.',
                   '',
                   '📝 Вставьте скопированный токен в сообщение этого чата:',
                   sep='\n'
    )
    reply_markup = InlineKeyboardBuilder()
    reply_markup.add(InlineKeyboardButton(text='⬅️ Назад', callback_data=f'settings_{seller_id}'))
    reply_markup.add(InlineKeyboardButton(text='🤵 Поддержка', url=config.bot.support_url))
    return text.as_html(), reply_markup.as_markup()

def inline_kb_del_apifbo(db_request, seller_id : int, employee_id : int,  tg_id : str):
    
    employee = db_request.get_employee(id=employee_id)
    seller = db_request.get_seller(id=seller_id)
    text = as_line(Bold('🗑 Удаление  '),
                   '',
                   '⚠️ Внимание! При выполнении этой команды из бота будет удален поставщик:',
                   f'🥝 {seller.name}',
                   '',
                   '⚠️ Статистика в отчётах бота также будет удалена.',
                   sep='\n'
    )
    text_and_data = [
        btn_back(f'apifbo_{seller_id}'),
        ['Удалить', f'delapifbo_accept_{seller_id}_{employee.id}'],
    ]
    schema = [2]
    reply_markup = InlineConstructor.create_kb(text_and_data=text_and_data, schema=schema)
    return text.as_html(), reply_markup

def inline_kb_apifbs(db_request, seller_id : int):
    seller = db_request.get_seller(id=seller_id)
    fbs_token = seller.token_fbs if seller.token_fbs else '⚠️ не установлен'
    text = as_line(Bold('🔑 API токен FBS (стандартный)  '),
                   '',
                   f'🥝 {seller.name}',
                   '',
                   'Если вы полностью или частично работаете по схеме FBS (продажа со склада поставщика), используйте дополнительный API токен (тип стандартный), чтобы WbNinjaBot мог отслеживать заказы.',
                   '',
                   '(Примечание: при этом первый API токен FBO (статистика) также используется, его удалять не нужно.)',
                   '',
                   '1️⃣ Зайдите в личный кабинет Личный кабинет WB → Настройки → Доступ к API (ссылка). ',
                   '',
                   '2️⃣ Нажмите кнопку [Создать новый токен]. Введите любое имя токена (например {bot_name}) и выберите тип Стандартный.',
                   '',
                   '3️⃣ Нажмите [Создать токен], а затем скопируйте его.',
                   '',
                   f'Текущий токен: {fbs_token}',
                   '',
                   '📝 Введите новый токен в этом сообщении:',
                   sep='\n'
    )
    text_and_data = []

    if seller.token_fbs:
        text_and_data.append(['Изменить токен', f'changeapifbs_accept_{seller_id}'])
        text_and_data.append(['Удалить токен', f'changeapifbs_accept_{seller_id}'])

    text_and_data.append(btn_back(f'settings_{seller_id}'))

    reply_markup = InlineConstructor.create_kb(text_and_data=text_and_data)
    return text.as_html(), reply_markup

def inline_kb_notifications(db_request, seller_id : int):
    seller = db_request.get_seller(id=seller_id)
    text = as_line(Bold('🔔 Настройка уведомлений'),
                   '',
                   f'🥝 {seller.name}',
                   sep='\n'
    )
    text_and_data = [
        ['Заказы', f'notiforders_{seller_id}'],
        ['Выкупы', f'notifbuyout_{seller_id}'],
        ['Отмены / Возвраты', f'notifcancel_{seller_id}'],
        btn_back(f'settings_{seller_id}')
    ]
    reply_markup = InlineConstructor.create_kb(text_and_data=text_and_data)
    return text.as_html(), reply_markup

def inline_kb_notiforders(db_request, employee_id : int, seller_id : int, button : str):
    text = Bold('🔔 Уведомления по заказам')
    text_and_data = [
        ['Показывать всё', f'notiforders_{seller_id}_all'],
        ['Если товар закончился', f'notiforders_{seller_id}_1'],
        ['Если товар заканчивается', f'notiforders_{seller_id}_2'],
        ['Если повышенная комиссия', f'notiforders_{seller_id}_3'],
        ['Если товар в избранном', f'notiforders_{seller_id}_4'],
        ['Отключить всё', f'notiforders_{seller_id}_none'],
        btn_back(f'notifications_{seller_id}')
    ]
    employee = db_request.get_employee(id=employee_id)

    if all([employee.order_notif_end, employee.order_notif_ending, employee.order_notif_commission, employee.order_notif_favorites]) \
        and button == 'all':
        text_and_data[0][0] = '👉 ' + text_and_data[0][0]
        text_and_data[1][1] = f'notiforders_{seller_id}_all_1'
        text_and_data[2][1] = f'notiforders_{seller_id}_all_2'
        text_and_data[3][1] = f'notiforders_{seller_id}_all_3'
        text_and_data[4][1] = f'notiforders_{seller_id}_all_4'

    elif all([not employee.order_notif_end, not employee.order_notif_ending, not employee.order_notif_commission, not employee.order_notif_favorites]):
        text_and_data[5][0] = '👉 ' + text_and_data[5][0]
    else:
        if employee.order_notif_end:
            text_and_data[1][0] = '👉 ' + text_and_data[1][0]
        if employee.order_notif_ending:
            text_and_data[2][0] = '👉 ' + text_and_data[2][0]
        if employee.order_notif_commission:
            text_and_data[3][0] = '👉 ' + text_and_data[3][0]
        if employee.order_notif_favorites:
            text_and_data[4][0] = '👉 ' + text_and_data[4][0]
    reply_markup = InlineConstructor.create_kb(text_and_data=text_and_data)
    return text.as_html(), reply_markup

def inline_kb_notifbuyout(db_request, employee_id : int, seller_id : int, button : str):
    text = Bold('🔔 Уведомления по выкупам')
    text_and_data = [
        ['Показывать всё', f'notifbuyout_{seller_id}_all'],
        ['Если товар закончился', f'notifbuyout_{seller_id}_1'],
        ['Если товар заканчивается', f'notifbuyout_{seller_id}_2'],
        ['Если повышенная комиссия', f'notifbuyout_{seller_id}_3'],
        ['Если товар в избранном', f'notifbuyout_{seller_id}_4'],
        ['Отключить всё', f'notifbuyout_{seller_id}_none'],
        btn_back(f'notifications_{seller_id}')
    ]
    employee = db_request.get_employee(id=employee_id)
    if all([employee.buyout_notif_end, employee.buyout_notif_ending, employee.buyout_notif_commission, employee.buyout_notif_favorites]) \
        and button == 'all':
        text_and_data[0][0] = '👉 ' + text_and_data[0][0]
        text_and_data[1][1] = f'notifbuyout_{seller_id}_all_1'
        text_and_data[2][1] = f'notifbuyout_{seller_id}_all_2'
        text_and_data[3][1] = f'notifbuyout_{seller_id}_all_3'
        text_and_data[4][1] = f'notifbuyout_{seller_id}_all_4'
    elif all([not employee.buyout_notif_end, not employee.buyout_notif_ending, not employee.buyout_notif_commission, not employee.buyout_notif_favorites]):
        text_and_data[5][0] = '👉 ' + text_and_data[5][0]
    else:
        if employee.buyout_notif_end:
            text_and_data[1][0] = '👉 ' + text_and_data[1][0]
        if employee.buyout_notif_ending:
            text_and_data[2][0] = '👉 ' + text_and_data[2][0]
        if employee.buyout_notif_commission:
            text_and_data[3][0] = '👉 ' + text_and_data[3][0]
        if employee.buyout_notif_favorites:
            text_and_data[4][0] = '👉 ' + text_and_data[4][0]
    reply_markup = InlineConstructor.create_kb(text_and_data=text_and_data)
    return text.as_html(), reply_markup

def inline_kb_notifcancel(db_request, employee_id : int, seller_id : int):
    text = Bold('🔔 Уведомления по отменам и возвратам')
    text_and_data = [
        ['Показывать всё', f'notifcancel_{seller_id}_1'],
        ['Отключить всё', f'notifcancel_{seller_id}_2'],
        btn_back(f'notifications_{seller_id}')
    ]
    employee = db_request.get_employee(id=employee_id)
    if employee.cancel_notif:
        text_and_data[0][0] = '👉 ' + text_and_data[0][0]
    else:
        text_and_data[1][0] = '👉 ' + text_and_data[1][0]
    reply_markup = InlineConstructor.create_kb(text_and_data=text_and_data)
    return text.as_html(), reply_markup

def inline_kb_balance(db_request, tg_id : str):
    user = db_request.get_user(tg_id=tg_id)
    sellers = db_request.get_seller(user_id=user.id)
    tariff = sum([s.tariff for s in sellers])
    text = as_line(Bold(f'💰 Баланс: {user.balance}₽'),
                   '',
                   f'· Ваш тариф: {tariff}₽ / мес',
                   f'· Поставщики: {len(sellers)}',
                   '',
                   '👨‍💼👩🏻‍💼 Если к вашему API-ключу подключены несколько сотрудников, то оплачивает кто-то один (администратор с положительным балансом), а пользуются все.',
                   '',
                   '🔒 Пополнение баланса производится только по Вашему согласию.',
                   '',
                   '🛡 Деньги с ваших карт в автоматическом режиме не списываются.',
                   '',
                   'ℹ️ Описание тарифов 👉🏻 /tariff',
                   sep='\n'
    )
    
    text_and_data = [
        [f'+ {tariff}₽', f'transaction_{tariff}']
    ]
    for i in [1, 3, 5, 10]:
        if i * 1000 > tariff:
            text_and_data.append([f'+ {i * 1000}₽', f'transaction_{i * 1000}'])
    schema = [1 for _ in text_and_data]
    button_type = ['callback_data' for _ in text_and_data]
    text_and_data.append(['Ввести купон', 'coupon'])
    text_and_data.append(['Пополнения', 'credit'])
    text_and_data.append(['Списания', 'debit'])
    text_and_data.append(['🤵 Поддержка', config.bot.support_url])
    text_and_data.append(btn_back('my'))
    schema += [1, 2, 1, 1]
    button_type += ['callback_data', 'callback_data', 'url', 'callback_data']
    
    reply_markup = InlineConstructor.create_kb(text_and_data=text_and_data, schema=schema, button_type=button_type)
    return text.as_html(), reply_markup
    
def inline_kb_payment(sum : int, payment_link : str):
    text = as_line(Bold(f'💰 Сумма к оплате: {sum}₽'),
                   '',
                   '🔒 Оплата полностью безопасна и производится на стороне платёжной системы.',
                   '',
                   '🇷🇺 Оплатить можно картой любого российского банка (Сбер, Тинькофф, Альфабанк и т.д.), а также Tinkoff Pay, СБП, ЯPAY.',
                   '',
                   '🇰🇿🇧🇾🇺🇿🇰🇬 Оплата для других стран также доступна, пишите в поддержку @SUPPORT!!!',
                   '',
                   '🕔 Средства на баланс бота поступают мгновенно.',
                   '',
                   '💪🏻 После оплаты бот активируется автоматически (в поддержку писать не нужно).',
                   sep='\n'
    )
    text_and_data = [
        ['Перейти к оплате', 'https://www.google.ru'],
        btn_back('balanсe')
    ]
    button_type = ['url', 'callback_data']
    reply_markup = InlineConstructor.create_kb(text_and_data=text_and_data, button_type=button_type)
    return text.as_html(), reply_markup

def inline_kb_credit(db_request, tg_id : str):
    user = db_request.get_user(tg_id=tg_id)
    transactions = db_request.get_transaction(user_id=user.id, type=False)
    text = as_line(Bold('🧾 Пополнения'),
                   '',
                   sep='\n'
    )
    if not transactions:
        text += 'Пополнений еще не было'
    else:
        for t in transactions:
            if t.type:
                bill = t.bill_link if t.bill_link.startswith('Купон') else TextLink(f'№{t.bill_number}', url=t.bill_link)
                text += f'Дата:                  {t.datetime.strftime("%d.%m.%Y %H:%M")}\nНомер:              {t.id}\nЗачислено:       {t.sum}₽\nКассовый чек:  {bill}\n\n'
    text_and_data = [
        btn_back('balanсe')
    ]
    reply_markup = InlineConstructor.create_kb(text_and_data=text_and_data)
    return text.as_html(), reply_markup

def inline_kb_debit(db_request, tg_id : str):
    user = db_request.get_user(tg_id=tg_id)
    transactions = db_request.get_transaction(user_id=user.id, type=False)
    text = as_line(Bold('🧾 Списания'),
                   '',
                   sep='\n'
    )
    if not transactions:
        text += 'Списания еще не было'
    else:
        for t in transactions:
            if not t.type:
                text += f'Номер:              {t.id}\nДата:                  {t.datetime.strftime("%d.%m.%Y %H:%M")}\nПоставщик:      {t.seller_name}\nТариф:               {t.tariff}\nБаланс:             {t.balance}\nЗачислено:       {t.sum}₽\n\n'
    text_and_data = [
        btn_back('balanсe')
    ]
    reply_markup = InlineConstructor.create_kb(text_and_data=text_and_data)
    return text.as_html(), reply_markup

def inline_kb_coupon():
    text = 'Введите название купона:'
    reply_markup = InlineConstructor.create_kb(text_and_data=[btn_back('balanсe')])
    return text, reply_markup

def inline_kb_tariff():
    text = as_line(Bold('💰 Тарифы {bot_name}'),
                   '',
                   'Тестовый бесплатный период для новых поставщиков составляет 14 дней (тестовый период начинает действовать с момента поступления первого заказа).',
                   '',
                   'Минимальная сумма для внесения на баланс составляет стоимость тарифа за 1 месяц. Оплату бот списывает с баланса каждые сутки за день работы. ',
                   '',
                   'Стоимость тарифа зависит от количества заказов за 30 дней до расчетной даты (пересчитывается 1 раз в месяц в расчетный день, независимо от даты пополнения баланса). ',
                   '',
                   'Ваша оплата в зависимости от количества заказов в месяц составит:',
                   '',
                   'От 1 до 300 = 290₽ / мес',
                   '', 
                   'От 301 до 1000 = 490₽ / мес', 
                   '', 
                   'От 1001 до 3000 = 790₽ / мес', 
                   '', 
                   'От 3001 до 10 000 = 1090₽ / мес', 
                   '', 
                   'От 10 001 до 100 000 = 1390₽ / мес', 
                   '', 
                   'От 100 001 = 1690₽ / мес ', 
                   '(+300₽ / мес за каждые дополнительные 100 000 продаж). ', 
                   '', 
                   'При подключении к боту нескольких кабинетов (API-ключей) тарифы суммируются.', 
                   '', 
                   'Наши преимущества', 
                   '', 
                   '✅ 👨‍💼👩🏻‍💼 За дополнительных сотрудников, подключённых к вашим API-ключам, оплата не взимается. ', 
                   '', 
                   '✅ 🐉 Заказы, полученные в режиме Дракона, не тарифицируются. ', 
                   '', 
                   '✅ 🔒 Оплата производится только по Вашему согласию.', 
                   '', 
                   '✅ 🛡 Деньги с карты в автоматическом режиме не списываются.', 
                   '', 
                   sep='\n'
    )

    text += as_line(f'📹 Как оплатить 👉🏻',
                    TextLink("видеоинструкция", url=config.bot.videoinstruction)
    )

    text += as_line('',
                    'ℹ️ Узнать текущий тариф 👉🏻 /balance',
                    sep='\n'
    )
    text_and_data = [
        ['Перейти к оплате', 'balanсe']
    ]
    reply_markup = InlineConstructor.create_kb(text_and_data=text_and_data)
    return text.as_html(), reply_markup
                   
def inline_kb_news(db_request, news_id : int = None, tg_id : str = None):
    text = '<b>НОВОСТИ</b>\n\n'
    news_ids = [n.id for n in db_request.get_news()]
    schema = None
    button_type = None
    if news_ids:
        current_news = db_request.get_news(id=news_id) if news_id else db_request.get_news(id=news_ids[-1])
        text += current_news.publication_date.strftime('%d.%m.%Y\n')
        text += current_news.text
        text_and_data = []
        if news_id == news_ids[-1] and len(news_ids) == 1:
            text_and_data = [['🤵 Поддержка', config.bot.support_url]]
        elif news_id == news_ids[-1] and len(news_ids) > 1:
            text_and_data.append(['Следующая ➡️', f'news_{news_ids[-2]}'])
        elif not news_id and len(news_ids) == 1:
            text_and_data = [['🤵 Поддержка', config.bot.support_url]]
        elif news_id == news_ids[0] and len(news_ids) > 1:
            text_and_data.append(['⬅️ Предыдущая', f'news_{news_ids[1]}'])
        else:
            next_id = news_ids[news_ids.index(news_id) - 1]
            prev_id = news_ids[news_ids.index(news_id) + 1]
            text_and_data.append(['⬅️ Предыдущая', f'news_{prev_id}'])
            text_and_data.append(['Следующая ➡️', f'news_{next_id}'])
            schema = [2]
    else:
        text += 'Новостей пока нет...'
        text_and_data = [['🤵 Поддержка', config.bot.support_url]]
        button_type = ['url']

    if db_request.get_user(tg_id=tg_id).is_admin:
        text_and_data.append(['Добавить новость', f'addnews_{news_id}'])
        if news_ids:
            news_id = news_ids[0] if not news_id else news_id
            id = news_ids[news_ids.index(news_id) - 1] if news_id != news_ids[0] and news_id != None else news_ids[0] if news_id != news_ids[0] else news_ids[1] if len(news_ids) > 1 else None
            text_and_data.append(['Удалить новость', f'delnews_{id}_{news_id}'])
        if schema:
            schema += [1, 1]
        if button_type:
            button_type += ['callback_data', 'callback_data']
    
    reply_markup = InlineConstructor.create_kb(text_and_data=text_and_data, schema=schema, button_type=button_type)
    return text, reply_markup

def inline_kb_addnews(news_id):
    text = 'Введите текст новости.\n\nЧтобы форматировать текст используйте HTML разметку.'
    reply_markup = InlineConstructor.create_kb(text_and_data=[btn_back(f'news_{news_id}')])
    return text, reply_markup

def inline_kb_stocks(db_request, tg_id : str):
    text = as_line(Bold('ТОВАРЫ И ОСТАТКИ'),
                   '',
                   sep='\n'
    )

    sellers = db_request.get_seller(user_id=db_request.get_user(tg_id=tg_id).id)
    is_selected = []
    for seller in sellers:
        employee = db_request.get_employee(seller_id=seller.id, user_id=db_request.get_user(tg_id=tg_id).id)
        is_selected.append(employee.is_selected)
        if employee.is_selected:
            products = db_request.get_product(seller_id=seller.id)
            product_warehouse = db_request.get_product_warehouse(seller_id=seller.id)
            quantity = sum([pw.quantity for pw in product_warehouse])
            inWayToClient = sum([pw.inWayToClient for pw in product_warehouse])
            inWayFromClient = sum([pw.inWayFromClient for pw in product_warehouse])

            text += as_line(Bold(seller.name),
                        f'📦 Остатки всего: {quantity}',
                        f'🚛 В пути до клиента: {inWayToClient}',
                        f'🚚 В пути возвраты: {inWayFromClient}',
                        f'🗂 Артикулы в продаже: {len(products)}',
                        '',
                        sep='\n'
            )
    
    text_and_data = [
        ['📦 Мои товары','myproducts_1'],
        ['💟 Избранное','favorites_1'],
        ['🗄 Архив','archive_1'],
    ]
    if len(sellers) > 1:
        btn = 'По всем поставщикам' if all(is_selected) else f'Выбрано поставщиков: {len([i for i in is_selected if i])}'
        text_and_data.insert(0, [btn,'selectseller_stock'])
    
    reply_markup = InlineConstructor.create_kb(text_and_data=text_and_data)
    return text.as_html(), reply_markup

def inline_kb_selectseller(db_request, tg_id : str, code : str = 'all', back : str = None):
    sellers = db_request.get_seller(user_id=db_request.get_user(tg_id=tg_id).id)
    text = as_line(Bold('Выбор поставщика'),
                   '',
                   'Выберите поставщиков, по которым хотите построить отчёт:',
                   sep='\n'
    )
    text_and_data = []
    is_selected = []
    for seller in sellers:
        employee = db_request.get_employee(seller_id=seller.id, user_id=db_request.get_user(tg_id=tg_id).id)
        is_selected.append(employee.is_selected)
        btn = f'👉 {seller.name}' if employee.is_selected else seller.name
        text_and_data.append([btn, f'selectseller_{back}_{seller.id}'])
    
    btn = [f'👉 По всем поставщикам', 'none'] if all(is_selected) and code == 'all' else ['По всем поставщикам', f'selectseller_{back}_all']
    text_and_data.append(btn)

    if all(is_selected) and code == 'all':
        text_and_data = [[tad[0].strip('👉 '), tad[1]] for tad in text_and_data[:-1]] + [text_and_data[-1]]
    text_and_data.append(btn_back(back))

    reply_markup = InlineConstructor.create_kb(text_and_data=text_and_data)
    return text.as_html(), reply_markup

def inline_kb_stock_myproducts(db_request, tg_id : str, page : int = 1, filter : str = None):
    title = 'МОИ ТОВАРЫ' if filter == 'myproducts' else 'ИЗБРАННОЕ' if filter == 'favorites' else 'АРХИВ'
    text = as_line(Bold(title),
                   sep='\n'
    )
    user = db_request.get_user(tg_id=tg_id)
    products_dcts = []
    total_revenue = {}
    seller_ids = [s.id for s in db_request.get_seller(user_id=user.id) if db_request.get_employee(seller_id=s.id, user_id=user.id).is_selected]
    for seller_id in seller_ids:
        products = db_request.get_product(seller_id=seller_id)
        for product in products:
            user_seller = db_request.get_employee(user_id=user.id, seller_id=product.seller.id)
            product_warehouse = db_request.get_product_warehouse(product_id=product.id)
            products_dct = {}
            products_dct['product'] = product
            products_dct['seller_id'] = seller_id
            products_dct["rating"] = product.rating
            products_dct["reviews"] = product.reviews
            products_dct['inWayToClient'] = sum([p.inWayToClient for p in product_warehouse])
            products_dct['inWayFromClient'] = sum([p.inWayFromClient for p in product_warehouse])
            products_dct['stock'] = sum([p.quantity for p in product_warehouse])
            products_dct['sales_list'] = db_request.get_sale(product_id=product.id, type='S', period=f"{(datetime.now() - timedelta(days=91)).strftime('%d.%m.%Y')} - {datetime.now().strftime('%d.%m.%Y')}")
            products_dct['sales'] = len(products_dct['sales_list']) - products_dct['inWayFromClient']
            gNumbers = [s['gNumber'] for s in products_dct['sales_list']]
            products_dct['orders_list'] = [o for o in db_request.get_order(product_id=product.id, period=f"{(datetime.now() - timedelta(days=91)).strftime('%d.%m.%Y')} - {datetime.now().strftime('%d.%m.%Y')}") if o['gNumber'] in gNumbers]
            products_dct['sales_revenue'] = sum([s['priceWithDisc'] for s in products_dct['sales_list']])
            try:
                total_revenue[seller_id] += products_dct['sales_revenue']
            except:
                total_revenue[seller_id] = products_dct['sales_revenue']
            try:
                products_dct['load'] = int((len(products_dct["orders_list"])/91) * user_seller.stock_reserve - products_dct["stock"])
            except:
                products_dct['load'] = 0
            try:
                products_dct['buyout'] = int((products_dct["sales"]/len(products_dct["orders_list"])) * 100)
            except:
                products_dct['buyout'] = 0
            products_dct['favorites'] = True if product.id in [p.id for p in db_request.get_product(in_favorites=user_seller.id)] else False            
            products_dct['archive'] = True if product.id in [p.id for p in db_request.get_product(in_archive=user_seller.id)] else False
            if filter == 'favorites':
                if products_dct['favorites']:
                    products_dcts.append(products_dct)
            elif filter == 'archive':
                if products_dct['archive']:
                    products_dcts.append(products_dct)
            else:
                products_dcts.append(products_dct)

    cumulative_total = {}
    products_dcts_revenue_sorted = sorted(products_dcts, key=lambda x:x['sales_revenue'], reverse=True)
    for seller_id in seller_ids:
        for product in products_dcts_revenue_sorted:
            if product['seller_id'] == seller_id:
                try:
                    product['abc'] = product['sales_revenue'] / total_revenue[product['seller_id']] * 100
                except:
                    product['abc'] = 0
                try:
                    cumulative_total[product['seller_id']] += product['abc']
                except:
                    cumulative_total[product['seller_id']] = product['abc']
                product['cumulative_total'] = cumulative_total[product['seller_id']]
                if cumulative_total[product['seller_id']] <= 80:
                    product['abc_key'] = 'A'
                elif 80 < cumulative_total[product['seller_id']] <= 95:
                    product['abc_key'] = 'B'
                else:
                    product['abc_key'] = 'C'
    
    key = str(user.stock_sorting).replace('StockSorting.', '').replace('ASC', '').replace('DESC', '')
    
    if 'ASC' in str(user.stock_sorting):
        products_dcts_sorted = sorted(products_dcts_revenue_sorted, key=lambda x:x[key])
    else:
        products_dcts_sorted = sorted(products_dcts_revenue_sorted, key=lambda x:x[key], reverse=True)

    addfavorites_code = 'addfav'
    delfavorites_code = 'delfav'
    for product in products_dcts_sorted[page * 10 - 10:page * 10]:    
        
        url = f"https://www.wildberries.ru/catalog/{product['product'].nmId}/detail.aspx"
        text += as_line('')
        text += as_line(f'🆔 Артикул WB: ',
                        TextLink(product["product"].nmId, url=url),
        )
        text += as_line(f'📁 {product["product"].subject}',
        )
        text += as_line(f'🏷 {product["product"].brand} / ',
                        TextLink(product["product"].supplierArticle, url=url)
        )
        try:
            days = int(product["stock"]/(len(product["orders_list"])/91))
        except:
            days = 0
        fill_stock_str = f'🚗 Пополните склад на {product["load"]} шт.' if product["load"] > 0 else ''
        text += as_line(f'⭐️ Рейтинг: {product["rating"]}',
                        f'💬 Отзывы: {product["reviews"]}',
                        f'💎 Выкуп за 3 мес: {product["buyout"]}% ({product["sales"]}/{len(product["orders_list"])})',
                        f'🟧 ABC-анализ: {product["abc_key"]} ({round(product["abc"], 2)}%)',
                        f'🚛 В пути до клиента: {product["inWayToClient"]}',
                        f'🚚 В пути возвраты: {product["inWayFromClient"]}',
                        f'📦 На складе: {product["stock"]} шт.',
                        f'🗓 Хватит на {days} дн.',
                        sep='\n'
        )
        if fill_stock_str:
            text += as_line(fill_stock_str)

        if product['favorites']:
            text += as_line(f'💟 ', TextLink('[– Убрать из избранного]', url=f'{config.bot.bot_url}?start=favorites_{product["product"].id}')
            )
            delfavorites_code += '_' + str(product["product"].id)
        else:
            text += as_line(f'💟 ', TextLink('[+ Добавить в избранное]', url=f'{config.bot.bot_url}?start=favorites_{product["product"].id}')
            )
            addfavorites_code += '_' + str(product["product"].id)
        if product['archive']:
            text += as_line(f'🗄 ', TextLink('[- Удалить из архива]', url=f'{config.bot.bot_url}?start=archive_{product["product"].id}')
            )
        else:
            text += as_line(f'🗄 ', TextLink('[+ Добавить в архив]', url=f'{config.bot.bot_url}?start=archive_{product["product"].id}')
            )
    
        
    if len(addfavorites_code.split('_')) == 1:
        addfavorites_text = '💔 Удалить всё из избранного'
        favorites_code = delfavorites_code
    else:
        addfavorites_text = '💟 Добавить всё в избранное'
        favorites_code = addfavorites_code
    
    text_and_data = [
        ['Продажи 🔺', f'{filter}_salesASC_1'],
        ['Продажи 🔻', f'{filter}_salesDESC_1'],
        ['Пополнить 🔺', f'{filter}_loadASC_1'],
        ['Пополнить 🔻', f'{filter}_loadDESC_1'],
        ['Остатки 🔺', f'{filter}_stockASC_1'],
        ['Остатки 🔻', f'{filter}_stockDESC_1'],
        ['Рейтинг 🔺', f'{filter}_ratingASC_1'],
        ['Рейтинг 🔻', f'{filter}_ratingDESC_1'],
        ['Отзывы 🔺', f'{filter}_reviewsASC_1'],
        ['Отзывы 🔻', f'{filter}_reviewsDESC_1'],
        ['Выкуп 🔺', f'{filter}_buyoutASC_1'],
        ['Выкуп 🔻', f'{filter}_buyoutDESC_1'],
        ['ABC-анализ 🔺', f'{filter}_abcASC_1'],
        ['ABC-анализ 🔻', f'{filter}_abcDESC_1'],
        [addfavorites_text, favorites_code],
        btn_back('stock'),
        ['🔍 Поиск', 'none'],
    ]
    for i in range(len(text_and_data)):
        if str(user.stock_sorting).strip('StockSorting.') in text_and_data[i][1]:
            text_and_data[i][0] = '🟢 ' + text_and_data[i][0]
    schema = [2, 2, 2, 2, 2, 2, 2, 1, 2]

    if filter in ['favorites', 'archive']:
        del text_and_data[-3]
        del schema[-2]

    for i in range(len(text_and_data)):
        if str(user.reports_groupby).replace('ReportsGroupBy.', '').lower() in text_and_data[i][1]:
            text_and_data[i][0] = '🟢 ' + text_and_data[i][0]
            text_and_data[i][1] = 'none' 
    if page == 1:
        if len(products_dcts_sorted) > 10:
            text_and_data.insert(0, ['След ➡️', f'{filter}_{page + 1}'])
            schema.insert(0, 1)
    elif page == (len(products_dcts_sorted) // 10) + 1 or page == len(products_dcts_sorted) // 10:
        text_and_data.insert(0, ['⬅️ Пред', f'{filter}_{page - 1}'])
        schema.insert(0, 1)
    else:
        text_and_data.insert(0, ['След ➡️', f'{filter}_{page + 1}'])
        text_and_data.insert(0, ['⬅️ Пред', f'{filter}_{page - 1}'])
        schema.insert(0, 2)

    reply_markup = InlineConstructor.create_kb(text_and_data=text_and_data, schema=schema)
    return text.as_html(), reply_markup

def inline_kb_reports(db_request, tg_id : str):
    text = as_line(Bold('СВОДКА'),
                   '',
                   sep='\n'
    )

    sellers = db_request.get_seller(user_id=db_request.get_user(tg_id=tg_id).id)
    is_selected = []
    for seller in sellers:
        employee = db_request.get_employee(seller_id=seller.id, user_id=db_request.get_user(tg_id=tg_id).id)
        is_selected.append(employee.is_selected)
        if employee.is_selected:
            today_orders = [o['totalPrice'] * (1 - o['discountPercent'] / 100) for o in db_request.get_order(seller_id=seller.id, period='today', select_for='reports')]
            yesterday_orders = [o['totalPrice'] * (1 - o['discountPercent'] / 100) for o in db_request.get_order(seller_id=seller.id, period='yesterday', select_for='reports')]
            week_orders = [o['totalPrice'] * (1 - o['discountPercent'] / 100) for o in db_request.get_order(seller_id=seller.id, period='week', select_for='reports')]
            month_orders = [o['totalPrice'] * (1 - o['discountPercent'] / 100) for o in db_request.get_order(seller_id=seller.id, period='month', select_for='reports')]

            today_sales = [s['priceWithDisc'] for s in db_request.get_sale(seller_id=seller.id, period='today', type='S', select_for='reports')]
            yesterday_sales = [s['priceWithDisc'] for s in db_request.get_sale(seller_id=seller.id, period='yesterday', type='S', select_for='reports')]
            week_sales = [s['priceWithDisc'] for s in db_request.get_sale(seller_id=seller.id, period='week', type='S', select_for='reports')]
            month_sales = [s['priceWithDisc'] for s in db_request.get_sale(seller_id=seller.id, period='month', type='S', select_for='reports')]

            today_returns = [s['priceWithDisc'] for s in db_request.get_sale(seller_id=seller.id, period='today', type='R', select_for='reports')]
            yesterday_returns = [s['priceWithDisc'] for s in db_request.get_sale(seller_id=seller.id, period='yesterday', type='R', select_for='reports')]
            week_returns = [s['priceWithDisc'] for s in db_request.get_sale(seller_id=seller.id, period='week', type='R', select_for='reports')]
            month_returns = [s['priceWithDisc'] for s in db_request.get_sale(seller_id=seller.id, period='month', type='R', select_for='reports')]
            text += as_line(f'🥝 {seller.name}',
                            '',
                            Bold('СЕГОДНЯ'),
                            f"🛒 Заказы:        {len(today_orders)} на {'{0:,}'.format(int(sum(today_orders))).replace(',', ' ')}₽",
                            f"💳 Выкупы:       {len(today_sales)} на {'{0:,}'.format(int(sum(today_sales))).replace(',', ' ')}₽",
                            f'↩️ Возвраты:    {len(today_returns)}',
                            '',
                            Bold('ВЧЕРА'),
                            f"🛒 Заказы:        {len(yesterday_orders)} на {'{0:,}'.format(int(sum(yesterday_orders))).replace(',', ' ')}₽",
                            f"💳 Выкупы:       {len(yesterday_sales)} на {'{0:,}'.format(int(sum(yesterday_sales))).replace(',', ' ')}₽",
                            f'↩️ Возвраты:    {len(yesterday_returns)}',
                            '',
                            Bold('ЗА 7 ДНЕЙ'),
                            f"🛒 Заказы:        {len(week_orders)} на {'{0:,}'.format(int(sum(week_orders))).replace(',', ' ')}₽",
                            f"💳 Выкупы:       {len(week_sales)} на {'{0:,}'.format(int(sum(week_sales))).replace(',', ' ')}₽",
                            f'↩️ Возвраты:    {len(week_returns)}',
                            '',
                            Bold('ЗА 30 ДНЕЙ'),
                            f"🛒 Заказы:        {len(month_orders)} на {'{0:,}'.format(int(sum(month_orders))).replace(',', ' ')}₽",
                            f"💳 Выкупы:       {len(month_sales)} на {'{0:,}'.format(int(sum(month_sales))).replace(',', ' ')}₽",
                            f'↩️ Возвраты:    {len(month_returns)}',
                            '',
                            sep='\n')
    text += as_line('ℹ️ Фактические данные могут отличаться.')
    text_and_data = [
        ['Сегодня','reports_today_1'],
        ['Вчера','reports_yesterday_1'],
        ['7 дней','reports_week_1'],
        ['30 дней','reports_month_1'],
        ['Другой период','reports_timedelta'],
        ['🛒 Заказы','reportorders_1'],
        ['💳 Выкупы','repsalesS_1'],
        ['↩️ Возвраты','repsalesR_1'],
        ['⛔ Штрафы','repsalesD_1']
    ]
    schema = [2, 2, 1, 2, 2]
    if len(sellers) > 1:
        btn = 'По всем поставщикам' if all(is_selected) else f'Выбрано поставщиков: {len([i for i in is_selected if i])}'
        text_and_data.insert(0, [btn, 'selectseller_reports'])
        schema.insert(0,  1)
    reply_markup = InlineConstructor.create_kb(text_and_data=text_and_data, schema=schema)
    return text.as_html(), reply_markup

def inline_kb_reports_byperiod(db_request, state, tg_id : str, period : str, page : int = 1, search : str = None):
    text_period = 'СЕГОДНЯ' if period == 'today' else 'ВЧЕРА' if period == 'yesterday' else '7 ДНЕЙ' if period == 'week' else '30 ДНЕЙ' if period == 'month' else period
    text = as_line(Bold(f'СТАТИСТИКА ЗА {text_period}'),
                   '',
                   sep='\n'
    )
    if search:
        text += as_line(Bold('Поиск: '), f'🔍 "{search}"\n', sep=' ')
    user = db_request.get_user(tg_id=tg_id)
    sellers = db_request.get_seller(user_id=user.id)
    is_selected = []
    today_orders = []
    today_sales = []
    today_returns = []
    text_for_sorting = {}
    if user.reports_groupby == ReportsGroupBy.WITHOUTGROUP:
        for seller in sellers:
            employee = db_request.get_employee(seller_id=seller.id, user_id=user.id)
            is_selected.append(employee.is_selected)
            if employee.is_selected:
                if search:
                    today_orders += [o['totalPrice'] * (1 - o['discountPercent'] / 100) for o in db_request.get_order(seller_id=seller.id, period=period, select_for='reports') if str(o['nmId']) == search or str(o['supplierArticle']) == search or str(o['brand']) == search or str(o['subject']) == search]
                    today_sales += [s['priceWithDisc'] for s in db_request.get_sale(seller_id=seller.id, period=period, type='S', select_for='reports') if str(s['nmId']) == search or str(s['supplierArticle']) == search or str(s['brand']) == search or str(s['subject']) == search]
                    today_returns += [s['priceWithDisc'] for s in db_request.get_sale(seller_id=seller.id, period=period, type='R', select_for='reports') if str(s['nmId']) == search or str(s['supplierArticle']) == search or str(s['brand']) == search or str(s['subject']) == search]
                else:
                    today_orders += [o['totalPrice'] * (1 - o['discountPercent'] / 100) for o in db_request.get_order(seller_id=seller.id, period=period, select_for='reports')]
                    today_sales += [s['priceWithDisc'] for s in db_request.get_sale(seller_id=seller.id, period=period, type='S', select_for='reports')]
                    today_returns += [s['priceWithDisc'] for s in db_request.get_sale(seller_id=seller.id, period=period, type='R', select_for='reports')]
        
        text += as_line(f"🛒 Заказы:        {len(today_orders)} на {'{0:,}'.format(int(sum(today_orders))).replace(',', ' ')}₽",
                        f"💳 Выкупы:       {len(today_sales)} на {'{0:,}'.format(int(sum(today_sales))).replace(',', ' ')}₽",
                        f'↩️ Возвраты:    {len(today_returns)}',
                        sep='\n'
        )
    elif user.reports_groupby == ReportsGroupBy.SUBJECT:
        for seller in sellers:
            employee = db_request.get_employee(seller_id=seller.id, user_id=user.id)
            is_selected.append(employee.is_selected)
            if employee.is_selected:
                if search:
                    orders = [o for o in db_request.get_order(seller_id=seller.id, period=period, select_for='reports') if str(o['nmId']) == search or str(o['supplierArticle']) == search or str(o['brand']) == search or str(o['subject']) == search]
                    sales = [s for s in db_request.get_sale(seller_id=seller.id, period=period, type='S', select_for='reports') if str(s['nmId']) == search or str(s['supplierArticle']) == search or str(s['brand']) == search or str(s['subject']) == search]
                    returns = [s for s in db_request.get_sale(seller_id=seller.id, period=period, type='R', select_for='reports') if str(s['nmId']) == search or str(s['supplierArticle']) == search or str(s['brand']) == search or str(s['subject']) == search]
                else:
                    orders = [o for o in db_request.get_order(seller_id=seller.id, period=period, select_for='reports')]
                    sales = [s for s in db_request.get_sale(seller_id=seller.id, period=period, type='S', select_for='reports')]
                    returns = [s for s in db_request.get_sale(seller_id=seller.id, period=period, type='R', select_for='reports')]
                
                for subject in list(set([o['subject'] for o in orders] + [s['subject'] for s in sales] + [r['subject'] for r in returns])):
                    subject_orders = [o['totalPrice'] * (1 - o['discountPercent'] / 100) for o in orders if o['subject'] == subject]
                    subject_sales = [s['priceWithDisc'] for s in sales if s['subject'] == subject]
                    subject_returns = [r['priceWithDisc'] for r in returns if r['subject'] == subject]
                    text_for_sorting[len(subject_orders)] = as_line(Bold(subject),
                                    f"🛒 Заказы:        {len(subject_orders)} на {'{0:,}'.format(int(sum(subject_orders))).replace(',', ' ')}₽",
                                    f"💳 Выкупы:       {len(subject_sales)} на {'{0:,}'.format(int(sum(subject_sales))).replace(',', ' ')}₽",
                                    f'↩️ Возвраты:    {len(subject_returns)}',
                                    '',
                                    sep='\n', 
                                    )
    elif user.reports_groupby == ReportsGroupBy.ARTICLES:
        for seller in sellers:
            employee = db_request.get_employee(seller_id=seller.id, user_id=user.id)
            is_selected.append(employee.is_selected)
            if employee.is_selected:
                
                if search:
                    orders = [o for o in db_request.get_order(seller_id=seller.id, period=period, select_for='reports') if str(o['nmId']) == search or str(o['supplierArticle']) == search or str(o['brand']) == search or str(o['subject']) == search]
                    sales = [s for s in db_request.get_sale(seller_id=seller.id, period=period, type='S', select_for='reports') if str(s['nmId']) == search or str(s['supplierArticle']) == search or str(s['brand']) == search or str(s['subject']) == search]
                    returns = [s for s in db_request.get_sale(seller_id=seller.id, period=period, type='R', select_for='reports') if str(s['nmId']) == search or str(s['supplierArticle']) == search or str(s['brand']) == search or str(s['subject']) == search]
                else:
                    orders = [o for o in db_request.get_order(seller_id=seller.id, period=period, select_for='reports')]
                    sales = [s for s in db_request.get_sale(seller_id=seller.id, period=period, type='S', select_for='reports')]
                    returns = [s for s in db_request.get_sale(seller_id=seller.id, period=period, type='R', select_for='reports')]
                

                for article in list(set([o['nmId'] for o in orders] + [s['nmId'] for s in sales] + [r['nmId'] for r in returns])):
                    article_orders = [o['totalPrice'] * (1 - o['discountPercent'] / 100) for o in orders if o['nmId'] == article]
                    article_sales = [s['priceWithDisc'] for s in sales if s['nmId'] == article]
                    article_returns = [r['priceWithDisc'] for r in returns if r['nmId'] == article]
                    text_for_sorting[len(article_orders)] = as_line(Underline(TextLink(article, url=f'https://www.wildberries.ru/catalog/{article}/detail.aspx')),
                                    f"🛒 Заказы:        {len(article_orders)} на {'{0:,}'.format(int(sum(article_orders))).replace(',', ' ')}₽",
                                    f"💳 Выкупы:       {len(article_sales)} на {'{0:,}'.format(int(sum(article_sales))).replace(',', ' ')}₽",
                                    f'↩️ Возвраты:    {len(article_returns)}',
                                    f'📁 {db_request.get_product(nmId=article).subject}',
                                    as_line(f"🏷 {seller.name} / ", Underline(TextLink(db_request.get_product(nmId=article).supplierArticle, url=f'https://www.wildberries.ru/catalog/{article}/detail.aspx'))),
                                    sep='\n', 
                                    )
    
    elif user.reports_groupby == ReportsGroupBy.BRANDS:
        
        for seller in sellers:
            employee = db_request.get_employee(seller_id=seller.id, user_id=user.id)
            is_selected.append(employee.is_selected)
            if employee.is_selected:
                if search:
                    orders = [o for o in db_request.get_order(seller_id=seller.id, period=period, select_for='reports') if str(o['nmId']) == search or str(o['supplierArticle']) == search or str(o['brand']) == search or str(o['subject']) == search]
                    sales = [s for s in db_request.get_sale(seller_id=seller.id, period=period, type='S', select_for='reports') if str(s['nmId']) == search or str(s['supplierArticle']) == search or str(s['brand']) == search or str(s['subject']) == search]
                    returns = [s for s in db_request.get_sale(seller_id=seller.id, period=period, type='R', select_for='reports') if str(s['nmId']) == search or str(s['supplierArticle']) == search or str(s['brand']) == search or str(s['subject']) == search]
                else:
                    orders = [o for o in db_request.get_order(seller_id=seller.id, period=period, select_for='reports')]
                    sales = [s for s in db_request.get_sale(seller_id=seller.id, period=period, type='S', select_for='reports')]
                    returns = [s for s in db_request.get_sale(seller_id=seller.id, period=period, type='R', select_for='reports')]
                

                for brand in list(set([o['brand'] for o in orders] + [s['brand'] for s in sales] + [r['brand'] for r in returns])):
                    brand_orders = [o['totalPrice'] * (1 - o['discountPercent'] / 100) for o in orders if o['brand'] == brand]
                    brand_sales = [s['priceWithDisc'] for s in sales if s['brand'] == brand]
                    brand_returns = [r['priceWithDisc'] for r in returns if r['brand'] == brand]
                    text_for_sorting[len(brand_orders)] = as_line(Bold(brand),
                                                                    f"🛒 Заказы:        {len(brand_orders)} на {'{0:,}'.format(int(sum(brand_orders))).replace(',', ' ')}₽",
                                                                    f"💳 Выкупы:       {len(brand_sales)} на {'{0:,}'.format(int(sum(brand_sales))).replace(',', ' ')}₽",
                                                                    f'↩️ Возвраты:    {len(brand_returns)}',
                                                                    '',
                                                                    sep='\n'
                    )

    elif user.reports_groupby == ReportsGroupBy.REGIONS:
        regions = {}
        for seller in sellers:
            employee = db_request.get_employee(seller_id=seller.id, user_id=user.id)
            is_selected.append(employee.is_selected)
            if employee.is_selected:
                if search:
                    orders = [o for o in db_request.get_order(seller_id=seller.id, period=period, select_for='reports') if str(o['nmId']) == search or str(o['supplierArticle']) == search or str(o['brand']) == search or str(o['subject']) == search]
                    sales = [s for s in db_request.get_sale(seller_id=seller.id, period=period, type='S', select_for='reports') if str(s['nmId']) == search or str(s['supplierArticle']) == search or str(s['brand']) == search or str(s['subject']) == search]
                    returns = [s for s in db_request.get_sale(seller_id=seller.id, period=period, type='R', select_for='reports') if str(s['nmId']) == search or str(s['supplierArticle']) == search or str(s['brand']) == search or str(s['subject']) == search]
                else:
                    orders = [o for o in db_request.get_order(seller_id=seller.id, period=period, select_for='reports')]
                    sales = [s for s in db_request.get_sale(seller_id=seller.id, period=period, type='S', select_for='reports')]
                    returns = [s for s in db_request.get_sale(seller_id=seller.id, period=period, type='R', select_for='reports')]
                
                for region in list(set([o['oblast'] for o in orders] + [s['regionName'] for s in sales] + [r['regionName'] for r in returns])):
                    region_orders = [o['totalPrice'] * (1 - o['discountPercent'] / 100) for o in orders if o['oblast'] == region]
                    region_sales = [s['priceWithDisc'] for s in sales if s['regionName'] == region]
                    region_returns = [r['priceWithDisc'] for r in returns if r['regionName'] == region]
                    try:
                        regions[region]
                        regions[region]['len_orders'] += len(region_orders)
                        regions[region]['sum_orders'] += sum(region_orders)
                        regions[region]['len_sales'] += len(region_sales)
                        regions[region]['sum_sales'] += sum(region_sales)
                        regions[region]['sum_sales'] += len(region_returns)
                    except:
                        regions[region] = {'len_orders' : len(region_orders), 'sum_orders' : sum(region_orders), 'len_sales' : len(region_sales), 'sum_sales' : sum(region_sales), 'len_returns' : len(region_returns)}
        for region, values in regions.items():
            text_for_sorting[values['len_orders']] = as_line(Bold(region),
                                                            f"🛒 Заказы:        {values['len_orders']} на {'{0:,}'.format(int(values['sum_orders'])).replace(',', ' ')}₽",
                                                            f"💳 Выкупы:       {values['len_sales']} на {'{0:,}'.format(int(values['sum_sales'])).replace(',', ' ')}₽",
                                                            f"↩️ Возвраты:    {values['len_returns']}",
                                                            '',
                                                            sep='\n'
            )

    elif user.reports_groupby == ReportsGroupBy.CATEGORIES:
        for seller in sellers:
            employee = db_request.get_employee(seller_id=seller.id, user_id=user.id)
            is_selected.append(employee.is_selected)
            if employee.is_selected:
                if search:
                    orders = [o for o in db_request.get_order(seller_id=seller.id, period=period, select_for='reports') if str(o['nmId']) == search or str(o['supplierArticle']) == search or str(o['brand']) == search or str(o['subject']) == search]
                    sales = [s for s in db_request.get_sale(seller_id=seller.id, period=period, type='S', select_for='reports') if str(s['nmId']) == search or str(s['supplierArticle']) == search or str(s['brand']) == search or str(s['subject']) == search]
                    returns = [s for s in db_request.get_sale(seller_id=seller.id, period=period, type='R', select_for='reports') if str(s['nmId']) == search or str(s['supplierArticle']) == search or str(s['brand']) == search or str(s['subject']) == search]
                else:
                    orders = [o for o in db_request.get_order(seller_id=seller.id, period=period, select_for='reports')]
                    sales = [s for s in db_request.get_sale(seller_id=seller.id, period=period, type='S', select_for='reports')]
                    returns = [s for s in db_request.get_sale(seller_id=seller.id, period=period, type='R', select_for='reports')]
                
                for category in list(set([o['category'] for o in orders] + [s['category'] for s in sales] + [r['category'] for r in returns])):
                    category_orders = [o['totalPrice'] * (1 - o['discountPercent'] / 100) for o in orders if o['category'] == category]
                    category_sales = [s['priceWithDisc'] for s in sales if s['category'] == category]
                    category_returns = [r['priceWithDisc'] for r in returns if r['category'] == category]
                    text_for_sorting[len(category_orders)] = as_line(Bold(category),
                                                                    f"🛒 Заказы:        {len(category_orders)} на {'{0:,}'.format(int(sum(category_orders))).replace(',', ' ')}₽",
                                                                    f"💳 Выкупы:       {len(category_sales)} на {'{0:,}'.format(int(sum(category_sales))).replace(',', ' ')}₽",
                                                                    f'↩️ Возвраты:    {len(category_returns)}',
                                                                    '',
                                                                    sep='\n'
                    )
                                                                    
    sorted_text_list = sorted(text_for_sorting.items(), reverse=True)
    for _, value in sorted_text_list[page * 10 - 10:page * 10]:
        text += value

    search_btn = ['❌ Поиск отмена', f'reportsdeny_{period}_1'] if search else ['🔍 Поиск', f'search_{period}_report']

    text_and_data = [
        ['Предметы', f'reports_subject_{period}_1'],
        ['Артикулы', f'reports_articles_{period}_1'],
        ['Бренды', f'reports_brands_{period}_1'],
        ['Регионы', f'reports_regions_{period}_1'],
        ['Категории', f'reports_categories_{period}_1'],
        ['Без группировки', f'reports_withoutgroup_{period}_1'],
        btn_back('reports'),
        search_btn,
    ]
    schema = [2, 2, 2, 2]
    for i in range(len(text_and_data)):
        if str(user.reports_groupby).replace('ReportsGroupBy.', '').lower() in text_and_data[i][1]:
            text_and_data[i][0] = '🟢 ' + text_and_data[i][0]
            text_and_data[i][1] = 'none' 
    if page == 1:
        if len(sorted_text_list) > 10:
            text_and_data.insert(0, ['След ➡️', f'reports_{period}_{page + 1}'])
            schema.insert(0, 1)
    elif page == (len(sorted_text_list) // 10) + 1 or page == len(sorted_text_list) // 10:
        text_and_data.insert(0, ['⬅️ Пред', f'reports_{period}_{page - 1}'])
        schema.insert(0, 1)
    else:
        text_and_data.insert(0, ['След ➡️', f'reports_{period}_{page + 1}'])
        text_and_data.insert(0, ['⬅️ Пред', f'reports_{period}_{page - 1}'])
        schema.insert(0, 2)
    
    reply_markup = InlineConstructor.create_kb(text_and_data=text_and_data, schema=schema)
    return text.as_html(), reply_markup

def inline_kb_reports_timedelta():
    text = as_line('📝 Введите дату или диапазон дат в этом сообщении:',
                   '\n\n',
                   as_line('Пример 1: ', Code('02.10.2023'), sep=' '),
                   '',
                   as_line('Пример 2: ', Code('18.09.2023 - 25.09.2023', sep=' ')),
                   sep='')
    text_and_data = [['⬅️ Отмена', 'delete_msg']]
    reply_markup = InlineConstructor.create_kb(text_and_data=text_and_data)
    return text.as_html(), reply_markup

def inline_kb_search():
    text = as_line("🔍 Искать можно по артикулу WB, артикулу поставщика,  бренду, названию предмета или региону.",
                   "",
                   "Введите поисковый запрос в этом сообщении: 👇🏻",
                   sep="\n")
    text_and_data = [['⬅️ Отмена', 'delete_msg']]
    reply_markup = InlineConstructor.create_kb(text_and_data=text_and_data)
    return text.as_html(), reply_markup

def inline_kb_orders(db_request, tg_id : str = None, page : int = None, search : str = None):
    user = db_request.get_user(tg_id=tg_id)
    text = as_line(Bold('ЗАКАЗЫ'))
    if search:
        text += as_line(Bold('Поиск: '), f'🔍 "{search}"\n', sep=' ')
    orders = db_request.get_order(tg_id=tg_id)
    
    if user.reports_groupby_period == ReportsGroupByPeriod.WITHOUTGROUP:
        grouped_orders = []
        for order in orders:
            if search:
                if str(order['nmId']) != search \
                    and str(order['supplierArticle']) != search \
                    and str(order['brand']) != search \
                    and str(order['subject']) != search:
                    continue
            grouped_orders.append(as_line(order['date'].strftime('%d.%m.%Y %H:%M'), 
                            '\n',
                            Bold(f"🛒 {int(order['totalPrice'] * (1 - order['discountPercent'] / 100))}₽"),
                            '\n',
                            f"🆔 {order['srid']}", 
                            '\n',
                            as_line(f"🆔 Артикул WB: ", TextLink(order['nmId'], url=f"https://www.wildberries.ru/catalog/{order['nmId']}/detail.aspx"), sep=''), 
                            f"📁 {order['subject']}",
                            '\n',
                            as_line(f"🏷 {order['brand']} / ", TextLink(order['supplierArticle'], url=f"https://www.wildberries.ru/catalog/{order['nmId']}/detail.aspx"), sep=''),
                            f"🌐 {order['oblast']}",
                            '\n',
                            f"📦 {order['warehouseName']}",
                            '\n'
                            ))
        if len(grouped_orders) == 0:
            text += as_line('Ничего не найдено!')
        for row in grouped_orders[page * 10 - 10: page * 10]:
            text += row
            
    
    else:
        grouped_orders = {}
        for order in orders:
            if search:
                if str(order['nmId']) != search \
                    and str(order['supplierArticle']) != search \
                    and str(order['brand']) != search \
                    and str(order['subject']) != search:
                    continue
            if user.reports_groupby_period == ReportsGroupByPeriod.DAYS:
                date = order['date'].strftime('%d.%m.%Y')
            elif user.reports_groupby_period == ReportsGroupByPeriod.WEEKS:
                date = f"Неделя {order['date'].isocalendar().week} {order['date'].year}"
            elif user.reports_groupby_period == ReportsGroupByPeriod.MONTHS:
                date = order['date'].strftime('%m.%Y')
            if date in grouped_orders:
                if order['nmId'] in grouped_orders[date]:
                    grouped_orders[date][order['nmId']] += [order]
                else:
                    grouped_orders[date][order['nmId']] = [order]
            else:
                grouped_orders[date] = {}
                grouped_orders[date][order['nmId']] = [order]
        counter = 1
        for key, value in grouped_orders.items():
            for dkey, dvalue in value.items():
                if counter <= page * 10 and counter >= page * 10 - 10:
                    price = [o['totalPrice'] * (1 - o['discountPercent'] / 100) for o in dvalue]
                    text += as_line(Italic(key),
                                    '\n',
                                    Bold(f"🛒 Всего: {len(dvalue)} на {int(sum(price))}₽"),
                                    '\n',
                                    as_line(f"🆔 Артикул WB: ", Underline(TextLink(dkey, url=f"https://www.wildberries.ru/catalog/{dkey}/detail.aspx")), sep=''),
                                    f"📁 {dvalue[0]['subject']}",
                                    '\n',
                                    as_line(f"🏷 {dvalue[0]['brand']} / ", Underline(TextLink(dvalue[0]['supplierArticle'], url=f"https://www.wildberries.ru/catalog/{dkey}/detail.aspx")), sep=''),
                                    f"💰 Цена: {int(sum(price)/len(price))}₽ (средняя)", 
                                    '\n',
                                    )
                counter += 1

        if len(grouped_orders) == 0:
            text += as_line('Ничего не найдено!')

    search_btn = ['❌ Поиск отмена', 'reportorders_deny_1'] if search else ['🔍 Поиск', 'search_orders']
    search_code = f'{search.replace(" ", "-20")}_' if search else ''
    text_and_data = [
        ['По дням', f'reportorders_{search_code}days_1'],
        ['По неделям', f'reportorders_{search_code}weeks_1'],
        ['По месяцам', f'reportorders_{search_code}months_1'],
        ['Без группировки', f'reportorders_{search_code}withoutgroup_1'],
        btn_back('reports'),
        search_btn,
    ]
    schema = [2,2,2]

    if page == 1:
        if len(grouped_orders) > 10:
            text_and_data.insert(0, ['След ➡️', f'reportorders_{search_code}{page + 1}'])
            schema.insert(0, 1)
    elif page == (len(grouped_orders) // 10) + 1 or page == len(grouped_orders) // 10:
        text_and_data.insert(0, ['⬅️ Пред', f'reportorders_{search_code}{page - 1}'])
        schema.insert(0, 1)
    else:
        text_and_data.insert(0, ['След ➡️', f'reportorders_{search_code}{page + 1}'])
        text_and_data.insert(0, ['⬅️ Пред', f'reportorders_{search_code}{page - 1}'])
        schema.insert(0, 2)

    for i in range(len(text_and_data)):
        if str(user.reports_groupby_period).replace('ReportsGroupByPeriod.', '').lower() in text_and_data[i][1]:
            text_and_data[i][0] = '🟢 ' + text_and_data[i][0]
            text_and_data[i][1] = 'none' 

    reply_markup = InlineConstructor.create_kb(text_and_data=text_and_data, schema=schema)
    return text.as_html(), reply_markup

def inline_kb_sales(db_request, tg_id : str = None, page : int = None, search : str = None, type : str = None):
    user = db_request.get_user(tg_id=tg_id)
    text = as_line(Bold('ВЫКУПЫ')) if type == 'S' else as_line(Bold('ВОЗВРАТЫ')) if type == 'R' else as_line(Bold('ШТРАФЫ'))
    if search:
        text += as_line(Bold('Поиск: '), f'🔍 "{search}"\n', sep=' ')
    sales = db_request.get_sale(tg_id=tg_id, type=type)
    
    if user.reports_groupby_period == ReportsGroupByPeriod.WITHOUTGROUP:
        grouped_sales = []
        for sale in sales:
            if search:
                if str(sale['nmId']) != search \
                    and str(sale['supplierArticle']) != search \
                    and str(sale['brand']) != search \
                    and str(sale['subject']) != search:
                    continue
            grouped_sales.append(as_line(sale['date'].strftime('%d.%m.%Y %H:%M'), 
                            '\n',
                            Bold(f"🛒 {int(sale['priceWithDisc'])}₽"),
                            '\n',
                            f"🆔 {sale['srid']}", 
                            '\n',
                            as_line(f"🆔 Артикул WB: ", TextLink(sale['nmId'], url=f"https://www.wildberries.ru/catalog/{sale['nmId']}/detail.aspx"), sep=''), 
                            f"📁 {sale['subject']}",
                            '\n',
                            as_line(f"🏷 {sale['brand']} / ", TextLink(sale['supplierArticle'], url=f"https://www.wildberries.ru/catalog/{sale['nmId']}/detail.aspx"), sep=''),
                            f"🌐 {sale['oblast']}",
                            '\n',
                            f"📦 {sale['warehouseName']}",
                            '\n'
                            ))
        if len(grouped_sales) == 0:
            text += as_line('Ничего не найдено!')
        for row in grouped_sales[page * 10 - 10: page * 10]:
            text += row
    
    else:
        grouped_sales = {}
        for sale in sales:
            if search:
                if str(sale['nmId']) != search \
                    and str(sale['supplierArticle']) != search \
                    and str(sale['brand']) != search \
                    and str(sale['subject']) != search:
                    continue
            if user.reports_groupby_period == ReportsGroupByPeriod.DAYS:
                date = sale['date'].strftime('%d.%m.%Y')
            elif user.reports_groupby_period == ReportsGroupByPeriod.WEEKS:
                date = f"Неделя {sale['date'].isocalendar().week} {sale['date'].year}"
            elif user.reports_groupby_period == ReportsGroupByPeriod.MONTHS:
                date = sale['date'].strftime('%m.%Y')
            if date in grouped_sales:
                if sale['nmId'] in grouped_sales[date]:
                    grouped_sales[date][sale['nmId']] += [sale]
                else:
                    grouped_sales[date][sale['nmId']] = [sale]
            else:
                grouped_sales[date] = {}
                grouped_sales[date][sale['nmId']] = [sale]
        counter = 1
        for key, value in grouped_sales.items():
            for dkey, dvalue in value.items():
                if counter <= page * 10 and counter >= page * 10 - 10:
                    price = [s['priceWithDisc'] for s in dvalue]
                    text += as_line(Italic(key),
                                    '\n',
                                    Bold(f"🛒 Всего: {len(dvalue)} на {int(sum(price))}₽"),
                                    '\n',
                                    as_line(f"🆔 Артикул WB: ", Underline(TextLink(dkey, url=f"https://www.wildberries.ru/catalog/{dkey}/detail.aspx")), sep=''),
                                    f"📁 {dvalue[0]['subject']}",
                                    '\n',
                                    as_line(f"🏷 {dvalue[0]['brand']} / ", Underline(TextLink(dvalue[0]['supplierArticle'], url=f"https://www.wildberries.ru/catalog/{dkey}/detail.aspx")), sep=''),
                                    f"💰 Цена: {int(sum(price)/len(price))}₽ (средняя)", 
                                    '\n',
                                    )
                counter += 1

        if len(grouped_sales) == 0:
            text += as_line('Ничего не найдено!')

    search_btn = ['❌ Поиск отмена', 'repsales_deny_1'] if search else ['🔍 Поиск', 'search_orders']
    search_code = f'{search.replace(" ", "-20")}_' if search else ''
    text_and_data = [
        ['По дням', f'repsales{type}_{search_code}days_1'],
        ['По неделям', f'repsales{type}_{search_code}weeks_1'],
        ['По месяцам', f'repsales{type}_{search_code}months_1'],
        ['Без группировки', f'repsales{type}_{search_code}withoutgroup_1'],
        btn_back('reports'),
        search_btn,
    ]
    schema = [2,2,2]

    if page == 1:
        if len(grouped_sales) > 10:
            text_and_data.insert(0, ['След ➡️', f'repsales{type}_{search_code}{page + 1}'])
            schema.insert(0, 1)
    elif page == (len(grouped_sales) // 10) + 1 or page == len(grouped_sales) // 10:
        text_and_data.insert(0, ['⬅️ Пред', f'repsales{type}_{search_code}{page - 1}'])
        schema.insert(0, 1)
    else:
        text_and_data.insert(0, ['След ➡️', f'repsales{type}_{search_code}{page + 1}'])
        text_and_data.insert(0, ['⬅️ Пред', f'repsales{type}_{search_code}{page - 1}'])
        schema.insert(0, 2)

    for i in range(len(text_and_data)):
        if str(user.reports_groupby_period).replace('ReportsGroupByPeriod.', '').lower() in text_and_data[i][1]:
            text_and_data[i][0] = '🟢 ' + text_and_data[i][0]
            text_and_data[i][1] = 'none' 

    reply_markup = InlineConstructor.create_kb(text_and_data=text_and_data, schema=schema)
    return text.as_html(), reply_markup

def inline_kb_new_order(db_request, order_id : int):
    order = db_request.get_order(id=order_id)
    product = db_request.get_product(id=order.product.id)
    price = order.totalPrice * (1 - order.discountPercent / 100)
    product_warehouse = db_request.get_product_warehouse(product_id=product.id)
    sales_list = db_request.get_sale(product_id=product.id, type='S', period=f"{(datetime.now() - timedelta(days=91)).strftime('%d.%m.%Y')} - {datetime.now().strftime('%d.%m.%Y')}")
    inWayToClient = sum([p.inWayToClient for p in product_warehouse])
    inWayFromClient = sum([p.inWayFromClient for p in product_warehouse])
    sales = len(sales_list) - inWayFromClient
    gNumbers = [s['gNumber'] for s in sales_list]
    orders = db_request.get_order(product_id=product.id, period=f"{(datetime.now() - timedelta(days=91)).strftime('%d.%m.%Y')} - {datetime.now().strftime('%d.%m.%Y')}")
    today_orders = [o['totalPrice'] * (1 - o['discountPercent'] / 100) for o in orders if o['date'].date() == datetime.now().date()]
    today_orders_such = [o['totalPrice'] * (1 - o['discountPercent'] / 100) for o in orders if o['date'].date() == datetime.now().date() and o['nmId'] == order.nmId]
    yesterday_orders_such = [o['totalPrice'] * (1 - o['discountPercent'] / 100) for o in orders if o['date'].date() == (datetime.now() - timedelta(days=1)).date() and o['nmId'] == order.nmId]
    orders_list = [o for o in orders if o['gNumber'] in gNumbers]
    buyout = int((sales/len(orders_list)) * 100)
    text = as_line(order.date,
                   f'🛒 Заказ [{len(today_orders)}]: {price}₽',
                   f'📈 Сегодня: {len(today_orders)} на {int(sum(today_orders))}₽',
                   f'🆔 Арт: {order.nmId} 👉🏻',
                   f'🛍️ WB скидка: {round(order.totalPrice * (order.discountPercent / 100), 2)}₽ ({order.discountPercent}%)',
                   f'📁 {product.subject}',
                   f'🏷 {product.brand} / {product.supplierArticle}',
                   f'⭐ Рейтинг: {product.rating}',
                   f'💬 Отзывы: {product.reviews}',
                   f'💵 Сегодня таких: {len(today_orders_such)} на {int(sum(today_orders_such))}₽',
                   f'💶 Вчера таких: {len(yesterday_orders_such)} на {int(sum(yesterday_orders_such))}₽',
                   '🟥 ABC-анализ: C (5.78%)',
                   f'💼 Комиссия базовая: {price * (1 - 19/100)}₽ (19%)',
                   '💥 Акция: ???',
                   f'💎 Выкуп за 3 мес: {buyout}% ({sales}/{len(orders_list)})',
                   f'🌐 {order.warehouseName} → {order.oblast}: ???₽',
                   f'🚛 В пути до клиента: {inWayToClient}',
                   f'🚚 В пути возвраты: {inWayFromClient}',
                   '📦 Алексин: ??? шт. хватит на ??? дн.',
                   '',
                   sep='\n'
                   )
    return text.as_html()