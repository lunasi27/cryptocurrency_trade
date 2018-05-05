from common.database import Database
from common.environment import Env
from gate.gate_api import GateIO


class GateDb(Database):
    def __init__(self, env):
        super(GateDb, self).__init__(env)
        self.ticker_field_dict = {'baseVolume':    'REAL', 
                                  'high24hr':      'REAL', 
                                  'highestBid':    'REAL', 
                                  'last':          'REAL', 
                                  'low24hr':       'REAL', 
                                  'lowestAsk':     'REAL', 
                                  'percentChange': 'REAL', 
                                  'quoteVolume':   'REAL'}

    def getAllTables(self):
        result = super(GateDb, self).getAllTables()
        return [i[0] for i in result]

    def createTable(self, pair):
        self.ticker_field_dict['time'] = "TimeStamp  NOT NULL  DEFAULT (datetime('now','localtime'))"
        print('Create table for %s' % pair, flush=True)
        super(GateDb, self).createTable(pair, self.ticker_field_dict)

    def createTbForNewPairs(self, pair_list):
        for pair in pair_list:
            self.createTable(pair)
        

if __name__ == '__main__':
       env = Env()
       db = GateDb(env)
       gate_query = GateIO(env.config.gate.api_query_url,
                           env.config.gate.api_key,
                           env.config.gate.scret_key)
       ticker_pairs = gate_query.pairs()
       db.createTbForNewPairs(ticker_pairs)
       print('Total pairs: %s' % len(ticker_pairs), flush=True)
