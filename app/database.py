from pony.orm import *
from config import *

db = Database()

class KeyWord(db.Entity):
    __table_name__ = "keyword"

    id = PrimaryKey(int, auto=True)
    keyword = Required(str)
    requests = Optional(int, nullable=True)
    search_1 = Optional(IntArray, nullable=True)
    search_2 = Optional(IntArray, nullable=True)
    search_3 = Optional(IntArray, nullable=True)
    total = Optional(int, nullable=True)
    is_today = Optional(bool, default=True)

db.bind(provider='postgres', user='postgres', password=PG_PASS, host=PG_HOST, database='ninja')

db.generate_mapping(create_tables=True)

    

