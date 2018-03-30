from common.singleton import Singleton


class Position(object):
    __metaclass__ = Singleton
    def __init__(self):
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
            self.quantity += can_buy_quantity
            self.market_value += self.buy_price * can_buy_quantity
            self.balance -= self.buy_price * can_buy_quantity
            print('Buy at: %s' % self.buy_price)
            self.show()

    def sell(self, pair):
        self.sell_price = pair[1]
        self.time = pair[2]
        if self.quantity != 0:
            self.market_value = self.sell_price * self.quantity 
            print('Sell at: %s' % self.sell_price)
            self.show()
            self.balance += self.market_value
            self.quantity = 0
            self.market_value = 0

    def show(self):
        print('Quantity: %s' % self.quantity)
        print('Balance: %s' % self.balance)
        print('Market: %s' % self.market_value)
        print('Total: %s' % (self.balance + self.market_value))
        print('Time: %s' % self.time)
        print('------------------------------')

    def ifStop(self):
        diff = self.balance + self.market_value - 100
        if diff/100 >= 0.3:
            return True
        else:
            return False
