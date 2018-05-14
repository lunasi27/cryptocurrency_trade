from mongoengine import Document
from mongoengine import StringField, FloatField, DateTimeField
import datetime


class Ticker(Document):
    pair          = StringField(required=True)
    ########ticker_field########
    baseVolume    = FloatField()
    high24hr      = FloatField()
    highestBid    = FloatField()
    last          = FloatField()
    low24hr       = FloatField()
    lowestAsk     = FloatField()
    percentChange = FloatField()
    quoteVolume   = FloatField()
    ############################
    date          = DateTimeField(default=datetime.datetime.now)

    meta = {
        'indexes': [
           'pair',
            'date',
            ('pair', 'date')
        ]
    }

    def save_if_need(self):
        if len(self.__class__.objects(pair=self.pair, date=self.date)) < 1:
            return self.save()
        else:
            return None

    def to_state(self):
        ticker_dic = self.to_mongo()
        ticker_dic.pop('_id')
        ticker_dic.pop('pair')
        ticker_dic.pop('date')
        return stock_dic.values()

    def to_dic(self):
        ticker_dic = self.to_mongo()
        ticker_dic.pop('_id')
        return stock_dic.values()

    @classmethod
    def get_k_data(cls, pair, start, end):
        return cls.objects(pair=pair, date__gte=start, date__lte=end).order_by('date')

    @classmethod
    def exist_in_db(cls, pair):
        return True if cls.objects(pair=pair)[:1].count() else False

