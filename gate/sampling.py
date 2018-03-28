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
        for pair in env.config.common.trade_pairs:
            try:
                # Sometime fetch market data may fail
                price_dict = gate_query.ticker(pair)
            except:
                print('Warn: gate_query() return out of time.', flush=True)
                continue
            if price_dict['result'] == 'true':
                price_dict.pop('result')
                db.insert(pair, price_dict)
                print('Info: Insert latest price(%s) into db.' % price_dict['last'], flush=True)
            else:
                print('Error: Fetch real time price failed.', flush=True)
                break
        time.sleep(10)
    #print(db.query('eos_usdt', {'*':''}))
    #print(db.query('btm_usdt', {'*':''}))
