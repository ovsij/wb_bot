from bot.database.enum import *
from bot.database.models import *

from bot.config import load_config
config = load_config('.env')


#db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
# локальная БД
#db.bind(provider='postgres', user=config.postgres.user, password=config.postgres.password, host='localhost', database=config.postgres.database)

# основная БД
db.bind(provider='postgres', user=config.postgres_server.user, password=config.postgres_server.password, host=config.postgres_server.host, database=config.postgres_server.database)

# основная БД с сервера
#db.bind(provider='postgres', user=config.postgres_server.user, password=config.postgres_server.password, host='localhost', database=config.postgres_server.database)

#db.drop_all_tables(with_all_data=True)
db.provider.converter_classes.append((Enum, EnumConverter))

db.generate_mapping(create_tables=True)
