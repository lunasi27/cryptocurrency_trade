from common.environment import Env
from gate.database import GateDb
from gate.gate_api import GateIO
import time
import pdb


if __name__ == '__main__':
    env = Env()
    db = GateDb(env)
    gate_query = GateIO(env.config.gate.api_query_url,
                           env.config.gate.api_key,
                           env.config.gate.scret_key)
    while(True):
        try:
            # Sometime fetch market data may fail
            tickers_price_dict = gate_query.tickers()
            if type(tickers_price_dict) is not dict:
                print('Not get dict:')
                print(tickers_price_dict)
                continue
        except:
            print('Warn: gate_query(tickers) return out of time.', flush=True)
            time.sleep(10)
            continue
        # Check if there are new pairs
        db_pair_list = db.getAllTables()
        diff_pair_list = [p for p in tickers_price_dict.keys() if p not in db_pair_list]
        if len(diff_pair_list) > 0:
            db.createTbForNewPairs(diff_pair_list)
        # Process ticker pairs
        for ticker_pair,price_dict in tickers_price_dict.items():
            # Process here
            if price_dict['result'] == 'true':
                price_dict.pop('result')
            else:
                print('Error: Fetch %s price failed, ignore it.' % ticker_pair, flush=True)
                continue
            #print('Insert new price (%s) of %s' % (price_dict['last'], ticker_pair), flush=True)
            db.insert(ticker_pair, price_dict)
        #print('Total insert pairs: %s' % len(tickers_price_dict), flush=True)
        # Take sample from market every 10 second
        time.sleep(10)
