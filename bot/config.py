from dataclasses import dataclass

from environs import Env


@dataclass
class Bot:
    token: str
    admin_ids: list
    support_url: str
    oferta: str
    bot_url: str
    videoinstruction : str

@dataclass
class Postgres:
    user : str
    password : str
    host : str
    database : str

@dataclass
class Config:
    bot: Bot
    postgres : Postgres

def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        bot=Bot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            support_url=env.str("SUPPORT_URL"),
            oferta=env.str("OFERTA"),
            bot_url=env.str("BOT_URL"),
            videoinstruction=env.str("VIDEOINSTRUCTION"),
        ),
        postgres=Postgres(
            user=env.str("DB_USER"),
            password=env.str("DB_PASSWORD"),
            host=env.str("DB_HOST"),
            database=env.str("DB_DATABASE"),
        )
    )