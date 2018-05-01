from common.database import Database
from common.environment import Env
from gate.gate_api import GateIO

ticker_field_dict = {'baseVolume':    'REAL', 
                     'high24hr':      'REAL', 
                     'highestBid':    'REAL', 
                     'last':          'REAL', 
                     'low24hr':       'REAL', 
                     'lowestAsk':     'REAL', 
                     'percentChange': 'REAL', 
                     'quoteVolume':   'REAL'}


if __name__ == '__main__':
       env = Env()
       db = Database(env)
       gate_query = GateIO(env.config.gate.api_query_url,
                           env.config.gate.api_key,
                           env.config.gate.scret_key)
       ticker_pairs = gate_query.pairs()
       for pair in ticker_pairs:
           ticker_field_dict['time'] = "TimeStamp  NOT NULL  DEFAULT (datetime('now','localtime'))"
           print('Create table for %s' % pair)
           db.createTable(pair, ticker_field_dict)
       print('Total pairs: %s' % len(ticker_pairs))
