from datetime import datetime, timedelta

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.formatting import *
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.config import load_config
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
    text_and_data.append(['❌ Удалить поставщика', f'delapifbo_{seller_id}'])
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

def inline_kb_apifbo(db_request, seller_id : int):
    seller = db_request.get_seller(id=seller_id)
    text = as_line(Bold('🔑 Управление токеном'),
                   '',
                   f'🥝 {seller.name}',
                   '',
                   '👇🏻 Выберите действие:',
                   sep='\n'
    )
    text_and_data = [
        ['Заменить API токен FBO (статистика)', f'changeapifbo_{seller_id}'],
        ['Удалить API токен FBO (статистика)', f'delapifbo_{seller_id}'],
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

def inline_kb_del_apifbo(db_request, seller_id : int):
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
        ['Удалить', f'delapifbo_accept_{seller_id}'],
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
    transactions = db_request.get_transaction(user_id=user.id)
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
    transactions = db_request.get_transaction(user_id=user.id)
    text = as_line(Bold('🧾 Списания'),
                   '',
                   sep='\n'
    )
    if not transactions:
        text += 'Списания еще не было'
    else:
        for t in transactions:
            if not t.type:
                text += f"· {t.datetime.strftime('%d.%m.%Y %H:%M:%S')} - {t.sum}₽"
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
        print(news_ids)
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
