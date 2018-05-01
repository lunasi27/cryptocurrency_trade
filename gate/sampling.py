from common.environment import Env
from common.database import Database
from gate.gate_api import GateIO
import time


if __name__ == '__main__':
    env = Env()
    db = Database(env)
    gate_query = GateIO(env.config.gate.api_query_url,
                           env.config.gate.api_key,
                           env.config.gate.scret_key)
    while(True):
        try:
            # Sometime fetch market data may fail
            tickers_price_dict = gate_query.tickers()
        except:
            print('Warn: gate_query(tickers) return out of time.', flush=True)
            continue
        # Process ticker pairs
        for ticker_pair,price_dict  in tickers_price_dict.items():
            # Process here
            if price_dict['result'] == 'true':
                price_dict.pop('result')
            else:
                print('Error: Fetch %s price failed, ignore it.' % ticker_pair, flush=True)
                continue
            print('Insert new price (%s) of %s' % (price_dict['last'], ticker_pair), flush=True)
            db.insert(ticker_pair, price_dict)
        print('Total insert pairs: %s' % len(tickers_price_dict), flush=True)
        # Take sample from market every 10 second
        time.sleep(10)
