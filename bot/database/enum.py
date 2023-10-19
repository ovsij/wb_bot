from enum import Enum
from pony.orm.dbapiprovider import StrConverter, Converter, IntConverter


class StockSorting(Enum):
    salesASC = 'salesASC'
    salesDESC = 'salesDESC'
    loadASC = 'loadASC'
    loadDESC = 'loadDESC'
    stockASC = 'stockASC'
    stockDESC = 'stockDESC'
    ratingASC = 'ratingASC'
    ratingDESC = 'ratingDESC'
    reviewsASC = 'reviewsASC'
    reviewsDESC = 'reviewsDESC'
    buyoutASC = 'buyoutASC'
    buyoutDESC = 'buyoutDESC'
    abcASC = 'abcASC'
    abcDESC = 'abcDESC'

    @staticmethod
    def from_str(label):
        if label == 'salesASC':
            return StockSorting.salesASC
        elif label == 'salesDESC':
            return StockSorting.salesDESC
        elif label == 'loadASC':
            return StockSorting.loadASC
        elif label == 'loadDESC':
            return StockSorting.loadDESC
        elif label == 'stockASC':
            return StockSorting.stockASC
        elif label == 'stockDESC':
            return StockSorting.stockDESC
        elif label == 'ratingASC':
            return StockSorting.ratingASC
        elif label == 'ratingDESC':
            return StockSorting.ratingDESC
        elif label == 'reviewsASC':
            return StockSorting.reviewsASC
        elif label == 'reviewsDESC':
            return StockSorting.reviewsDESC
        elif label == 'buyoutASC':
            return StockSorting.buyoutASC
        elif label == 'buyoutDESC':
            return StockSorting.buyoutDESC
        elif label == 'abcASC':
            return StockSorting.abcASC
        elif label == 'abcDESC':
            return StockSorting.abcDESC
        else:
            raise NotImplementedError

class ReportsGroupBy(Enum):
    SUBJECT = 'subject'
    ARTICLES = 'articles'
    BRANDS = 'brands'
    REGIONS = 'regions'
    CATEGORIES = 'categories'
    WITHOUTGROUP = 'withoutgroup'

    @staticmethod
    def from_str(label):
        if label == 'subject':
            return ReportsGroupBy.SUBJECT
        if label == 'articles':
            return ReportsGroupBy.ARTICLES
        if label == 'brands':
            return ReportsGroupBy.BRANDS
        if label == 'regions':
            return ReportsGroupBy.REGIONS
        if label == 'categories':
            return ReportsGroupBy.CATEGORIES
        if label == 'withoutgroup':
            return ReportsGroupBy.WITHOUTGROUP

class ReportsGroupByPeriod(Enum):
    DAYS = 'days'
    WEEKS = 'weeks'
    MONTHS = 'months'
    WITHOUTGROUP = 'withoutgroup'

    @staticmethod
    def from_str(label):
        if label == 'days':
            return ReportsGroupByPeriod.DAYS
        if label == 'weeks':
            return ReportsGroupByPeriod.WEEKS
        if label == 'months':
            return ReportsGroupByPeriod.MONTHS
        if label == 'withoutgroup':
            return ReportsGroupByPeriod.WITHOUTGROUP

class EnumConverter(StrConverter):

    def validate(self, val, obj=None):
        if not isinstance(val, Enum):
            raise ValueError('Must be an Enum.  Got {}'.format(type(val)))
        return val

    def py2sql(self, val):
        return val.name

    def sql2py(self, value):
        # Any enum type can be used, so py_type ensures the correct one is used to create the enum instance
        return self.py_type[value]
    