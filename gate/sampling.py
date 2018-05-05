from common.environment import Env
from gate.database import GateDb
from gate.gate_api import GateIO
import time
import pdb


class Sampling(object):
    def __init__(self):
        env = Env()
        self.db = GateDb(env)
        self.gate_query = GateIO(env.config.gate.api_query_url,
                                 env.config.gate.api_key,
                                 env.config.gate.scret_key)

    def getTickerPrice(self):
        self.tickers_price = self.gate_query.tickers()
        # Sometime fetch market data may fail
        if type(self.tickers_price) is not dict:
            return False
        return True

    def check4NewPairs(self):
        db_pair_list = self.db.getAllTables()
        diff_pair_list = [p for p in self.tickers_price.keys() if p not in db_pair_list]
        if len(diff_pair_list) > 0:
            self.db.createTbForNewPairs(diff_pair_list)

    def saveTickerPairs(self):
        for ticker_pair,price_dict in self.tickers_price.items():
            if price_dict['result'] == 'true':
                price_dict.pop('result')
            else:
                print('WARN: Fetch %s failed, ignore it ...' % ticker_pair, flush=True)
                continue
            if self.isValidValue(price_dict):
                self.db.insert(ticker_pair, price_dict)


    def isValidValue(self, price_dict):
        if None in price_dict.values():
            return False
        return True

    def takeSample(self):
        while(True):
            try:
                # Collect ticker price data from market
                if not self.getTickerPrice():
                    print('WARN: Tickers price formate does not correct. Try again ...', flush=True)
                    time.sleep(10)
                    continue
            except:
                print('WARN: Get tikers price failed, try again ...', flush=True)
                time.sleep(10)
                continue
            # Check if there are new pairs
            self.check4NewPairs()
            # Process ticker pairs
            self.saveTickerPairs()
            # show take sample time stamp
            time_stamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            print('INFO: Take sample at %s ...' % time_stamp, flush=True)
            # Take sample from market every 10 second
            time.sleep(10)



if __name__ == '__main__':
    sp = Sampling()
    sp.takeSample()
