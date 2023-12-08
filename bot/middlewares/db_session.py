from datetime import datetime
import logging
from typing import Callable, Awaitable, Dict, Any, Union

from aiogram import BaseMiddleware, types
from aiogram.types import Update, CallbackQuery

from bot.config import Config, load_config
from bot.database.database import *
from bot.database.functions.db_requests import DbRequests


class DbSessionMiddleware(BaseMiddleware):
    @db_session()
    def __init__(self):
        super().__init__()

    
    async def __call__(self,
                       handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
                       event: Union[Message, CallbackQuery],
                       data: Dict[str, Any],
                       ) -> Any:
        db_requests = DbRequests()
        data["db_request"] = db_requests
        msg_text = None
        if event.message:
            tg_user: types.User = event.message.from_user
            msg_text = event.message.text
        elif event.callback_query:
            tg_user: types.User = event.callback_query.from_user
        user = db_requests.get_user(tg_id=str(tg_user.id))
        data["user"] = user
        # register user if not exists
        if not user:
            config: Config = load_config('.env')
            refer = db_requests.get_user(tg_id=msg_text.strip('/start ').split('_')[1]).id if msg_text and len(msg_text.split('_')) > 1 else None
            if tg_user.id in config.bot.admin_ids:
                user = db_requests.create_user(tg_user, refer_id=refer, is_admin=True)
            else:
                user = db_requests.create_user(tg_user, refer_id=refer)
            logging.info(f"new user {tg_user.id} ({tg_user.full_name}) in db")
        # update user data if changed
        try:
            if user.username != tg_user.username or \
                    user.first_name != tg_user.first_name or \
                    user.last_name != tg_user.last_name:
                db_requests.update_user(tg_id=str(tg_user.id),
                                        updated_fields={
                                            "username": tg_user.username,
                                            "first_name": tg_user.first_name,
                                            "last_name": tg_user.last_name,
                                            "last_use": datetime.now()
                                        })
            else:
                db_requests.update_user(
                    tg_id=str(tg_user.id),
                    updated_fields={
                    "last_use": datetime.now()
                    })
        except:
            pass
            
        return await handler(event, data)