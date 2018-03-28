from common.singleton import Singleton


class Position(object):
    __metaclass__ = Singleton
    def __init__(self, pair_name):
        self.pair_name = pair_name
        self.market_value = 0
        self.balance = 100
        self.quantity = 0
        #self.pair_name = ''
        self.buy_price = 0
        self.sell_price = 0
        self.time = None

    def buy(self, pair):
        self.buy_price = pair[1]
        self.time = pair[2]
        can_buy_quantity = int(self.balance / self.buy_price)
        if can_buy_quantity != 0:
            self.quantity = can_buy_quantity
            self.market_value = self.buy_price * self.quantity
            self.balance -= self.market_value
            print('Buy at: %s' % self.buy_price, flush=True)
            self.show()

    def sell(self, pair):
        self.sell_price = pair[1]
        self.time = pair[2]
        if self.quantity != 0:
            self.market_value = self.sell_price * self.quantity 
            print('Sell at: %s' % self.sell_price, flush=True)
            self.show()
            self.balance += self.market_value
            self.quantity = 0
            self.market_value = 0

    def show(self):
        print('Trade pair: %s' % self.pair_name, flush=True)
        print('Quantity: %s' % self.quantity, flush=True)
        print('Balance: %s' % self.balance, flush=True)
        print('Market: %s' % self.market_value, flush=True)
        print('Total: %s' % (self.balance + self.market_value), flush=True)
        print('Time: %s' % self.time, flush=True)
        print('------------------------------', flush=True)

    def ifStop(self):
        diff = self.balance + self.market_value - 100
        if diff/100 >= 0.3:
            return True
        else:
            return False
