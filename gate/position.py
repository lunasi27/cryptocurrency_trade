from common.position import Position
from gate.gate_api import GateIO
import time
import pdb


class GatePosition(Position):
    def __init__(self, env, pair_name):
        super(GatePosition, self).__init__(pair_name)
        # Make connection witg trade center
        self.gate_query = GateIO(env.config.gate.api_query_url,
                                 env.config.gate.api_key,
                                 env.config.gate.scret_key)

    def buy(self, _):
        while(True):
            buy_plan = self.makeBuyPlan()
            if buy_plan:
                print('Buy at: %s  Num: %s' % buy_plan)
                self.show()
                break

    def makeBuyPlan(self):
        # Find current sell price and market deeps
        market_deep_dict = self.gate_query.orderBook(self.pair_name)
        # Check result is valide
        if market_deep_dict['result'] != 'true':
            return False
        # ask_list is sell price deeps
        ask_list = market_deep_dict['asks']
        ask_list.reverse()
        # Only search top 1 sell price
        price, quantity = ask_list[0]
        can_buy_quantity = self.balance / price
        # Check how many you can buy
        if can_buy_quantity == 0:
            return False
        else:
            # Check market deeps
            if can_buy_quantity <= quantity:
                # Generate buy plan
                self.quantity += can_buy_quantity
            else:
                # Market deeps is not enough, shopping spree, others buy next time 
                can_buy_quantity = quantity
                self.quantity += can_buy_quantity
            # Update mark_value
            new_market_value = price * can_buy_quantity
            # Trade fee will make you more cost
            self.balance -= new_market_value * (1 + 0.002)
            self.market_value += new_market_value 
            return price, can_buy_quantity

    def sell(self, _):
        while(True):
            sell_plan = self.makeSellPlan()
            if sell_plan:
                print('Sell at: %s  Num: %s' % sell_plan)
                self.show()
                break

    def makeSellPlan(self):
        # Find current buy price and market deeps
        market_deep_dict = self.gate_query.orderBook(self.pair_name)
        # Check result is valide
        if market_deep_dict['result'] != 'true':
            return False
        # bid_list is the buy price deeps
        bid_list = market_deep_dict['bids']
        # Only search top 1 buy price
        price, quantity = bid_list[0]
        # Check how many you can sell
        can_sell_quantity = self.quantity
        if can_sell_quantity == 0:
            return False
        else:
            # Check market deeps
            if can_sell_quantity <= quantity:
                # Update mark_value
                new_balance_value = price * can_sell_quantity
                # Trade fee will make you more cost
                self.balance += new_balance_value * (1 - 0.002)
                # update global quantity
                self.quantity = 0
                self.market_value = 0
            else:
                # Market deep is not enough, shopping spree, others sell next time
                can_sell_quantity = quantity
                self.quantity -= can_sell_quantity
                # Update mark_value
                new_balance_value = price * can_sell_quantity
                # Trade fee will make you more cost
                self.balance += new_balance_value * (1 - 0.002)
                self.market_value -= new_balance_value
            # Return sell plan
            return price, can_sell_quantity

    def show(self):
        print('Trade pair: %s' % self.pair_name, flush=True)
        print('Quantity: %s' % self.quantity, flush=True)
        print('Balance: %s' % self.balance, flush=True)
        print('Market: %s' % self.market_value, flush=True)
        print('Total: %s' % (self.balance + self.market_value), flush=True)
        op_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        print('Time: %s' % op_time, flush=True)
        print('------------------------------', flush=True)



if __name__ == '__main__':
    from common.environment import Env
    env = Env()
    gp = GatePosition(env, 'eos_usdt')
    gp.buy('x')
    gp.sell('x')
    pass
