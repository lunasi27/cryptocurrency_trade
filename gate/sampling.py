from common.environment import Env
from gate.gate_db import Ticker
from gate.gate_api import GateIO
import time
import pdb


class Sampling(object):
    def __init__(self):
        env = Env()
        self.gate_query = GateIO(env.config.gate.api_query_url,
                                 env.config.gate.api_key,
                                 env.config.gate.scret_key)

    def getTickerPrice(self):
        self.tickers_price = self.gate_query.tickers()
        # Sometime fetch market data may fail
        if type(self.tickers_price) is not dict:
            return False
        return True

    def saveTickerPairs(self):
        for ticker_pair,price_dict in self.tickers_price.items():
            if price_dict['result'] == 'true':
                price_dict.pop('result')
            else:
                print('WARN: Fetch %s failed, ignore it ...' % ticker_pair, flush=True)
                continue
            if self.isValidValue(price_dict):
                price_dict = {x:float(y) for x,y in price_dict.items()}
                self.insertIntoDb(ticker_pair, price_dict)

    def insertIntoDb(self, ticker_pair, price_dict):
        tk = Ticker()
        tk.pair = ticker_pair
        tk.baseVolume = price_dict['baseVolume']
        tk.high24hr = price_dict['high24hr']
        tk.highestBid = price_dict['highestBid']
        tk.last = price_dict['last']
        tk.low24hr = price_dict['low24hr']
        tk.lowestAsk = price_dict['lowestAsk']
        tk.percentChange = price_dict['percentChange']
        tk.quoteVolume = price_dict['quoteVolume']
        tk.save_if_need()

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
            #self.check4NewPairs()
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
