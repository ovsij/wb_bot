from aiogram import Dispatcher, Router, F

from bot.config import Config
from bot.database.functions.db_requests import DbRequests
from bot.routers.admins.commands import admin_commands_router
from bot.routers.admins.callbacks import admin_callbacks_router
from bot.routers.admins.messages import admin_messages_router
from bot.routers.users.commands import user_commands_router
from bot.routers.users.calbacks import user_callbacks_router
from bot.routers.users.messages import user_messages_router
from bot.routers.chats.commands import chat_commands_router
from bot.routers.chats.calbacks import chat_callbacks_router


def register_all_routes(dp: Dispatcher, config: Config) -> None:
    master_router = Router()
    user_router = Router()
    admin_router = Router()
    chat_router = Router()
    dp.include_router(master_router)

    master_router.include_router(user_router)

    user_router.include_router(admin_router)
    master_router.include_router(chat_router)
    

    user_router.message.filter(F.chat.type.in_(['private']))
    user_router.callback_query.filter(F.message.chat.type.in_(['private']))
    user_router.include_router(user_commands_router)
    user_router.include_router(user_callbacks_router)
    user_router.include_router(user_messages_router)

    
    
    # Administrator routers
    db_requests = DbRequests()
    admin_router.message.filter(F.from_user.id.in_([int(u.tg_id) for u in db_requests.get_user(is_admin=True)]))
    admin_router.callback_query.filter(F.from_user.id.in_([int(u.tg_id) for u in db_requests.get_user(is_admin=True)]))
    

    admin_router.include_router(admin_commands_router)
    admin_router.include_router(admin_callbacks_router)
    admin_router.include_router(admin_messages_router)


    # Chat routers
    chat_router.message.filter(F.chat.type.in_(['group', 'supergroup']))
    chat_router.callback_query.filter(F.message.chat.type.in_(['group', 'supergroup']))
    chat_router.include_router(chat_commands_router)
    chat_router.include_router(chat_callbacks_router)
