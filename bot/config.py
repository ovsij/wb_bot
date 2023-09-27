from dataclasses import dataclass

from environs import Env


@dataclass
class Bot:
    token: str
    admin_ids: list[int]
    support_url: str
    oferta: str
    bot_url: str
    videoinstruction : str

@dataclass
class Config:
    bot: Bot

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
        )
    )