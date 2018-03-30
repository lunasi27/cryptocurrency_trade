
from common.database import Database
from common.position import Position
import matplotlib.pyplot as plt
import numpy as np
import time
import pdb

class Polynomial(object):
    def __init__(self, x, y):
        self.x = np.array(x)
        self.y = np.array(y)
        self.degree = 2

#    def show(self):
#        y_predit = self.poly1d(self.x)
#        y_df1 = self.df_1(self.x)
#        plt.figure('111')
#        plt.scatter(self.x, self.y, color='g', label='scatter')
#        plt.plot(self.x, self.y, color='r', label='line')
#        plt.plot(self.x, y_predit, color='b',label='fit')
#        plt.figure('222')
#        plt.plot(self.x, y_df1, color='y',label='df_1')
#        plt.show()
        
    def fit(self):
        poly_expression = np.polyfit(self.x, self.y, self.degree)
        self.poly1d = np.poly1d(poly_expression)
#        print(self.poly1d)
        self.df_1 = np.poly1d.deriv(self.poly1d)
        self.df_2 = np.poly1d.deriv(self.df_1)

    def maxOrMin(self):
        # First derivative
        self.df_1 = np.poly1d.deriv(self.poly1d)
        # Find max/min points
        #latest_solution = self.df_1.r.max()
        latest_solution = int(self.df_1.r.max())
        # Ingore image root
        if type(latest_solution) == np.complex128:
            print('Image root has found.') 
            return False
        # Only take care about min/max point bigger window
        if latest_solution >= self.x[0]:
            # Second derivative
            df_2 = np.poly1d.deriv(self.df_1)
            if df_2(latest_solution) == 0:
                # How to deal with stop point(Second derivative = 0)?
                print('Second derivative == 0.') 
                return False
            elif df_2(latest_solution) > 0:
                # Second derivative >0 means min point of original curve
                #print('(%s, Min)' % latest_solution)
                # Only pickup min point which bigger than max x of window
                return latest_solution, 'Min'
            else:
                # Second derivative <0 means max point of original curve
                #print('(%s, Max)' % latest_solution)
                # Only pickup max point which smaller than min x of window
                return latest_solution, 'Max'
        else:
            #print('Root out of range. %s' % latest_solution) 
            return False
        

class MovePloyFit(object):
    def __init__(self, env, window_size=90, step=1):
        #self.env = env
        self.db = Database(env)
        self.window_size = window_size
        self.step = step
        self.pre_status = (1,'Max')
        self.x = []
        self.y = []

    def setupPosition(self, pair):
        return Position(pair)

    def execute(self, data, pos):
        for pair in data:
            # Check if begin analysis
            if len(self.x) == self.window_size:
                poly = Polynomial(self.x, self.y)
                poly.fit()
                #print('x=%s, y=%s' % (self.x[-1], self.y[-1]))
                check_point = poly.maxOrMin()
                # Find min/max point
                if check_point:
                    # Current extremum status != previous extremum status
                    if check_point[1] != self.pre_status[1]:
                        # Previous fit center point must samller than right side of window
                        if self.pre_status[0] < self.x[-1]:
                            # Trend change, remove pre_fit half curve
                            self.x = self.x[self.pre_status[0]:]
                            self.y = self.y[self.pre_status[0]:]
                            self.pre_status = check_point
                    if check_point[1] == 'Min':
                        # Only buy when more than 40% points smaller than predict
                        if self.belowCheck(poly.poly1d) < 0.4:
                            # Min point find, Buy process
                            self.pos.buy(pair)
                    else:
                        # Only sell when more than 70% points samller than predict
                        if self.belowCheck(poly.poly1d) > 0.7:
                            # Max point find, Sell process
                            self.pos.sell(pair)
                #poly.show()
                self.x = self.x[self.step:]
                self.y = self.y[self.step:]
            # Just fill x,y list
            self.x.append(pair[0])
            self.y.append(pair[1])

    def belowCheck(self, poly1d):
        count = 0
        window_size = len(self.x)
        statistic_range = int(window_size / 6)
        for index in range(statistic_range):
            x = self.x[window_size - index - 1]
            y = self.y[window_size - index - 1]
            pred_y = poly1d(x)
            if y < pred_y:
                count += 1
#        print('small rate: %s' % (count / window * 100))
        return count / statistic_range
        # Sell 70%, buy 40%

    def regression(self, trade_pair='eos_usdt'):
        pos = self.setupPosition(trade_pair)
        sql = 'select rowid,last,time from %s' % trade_pair
        result = self.db.execute(sql, pos)
        data = result.fetchall()
        self.execute(data)
        pos.show()

    def realtime(self, trade_pair='eos_usdt'):
        pos = self.setupPosition(trade_pair)
        pos.show()
        # call select every <xxx> second
        row_id = 0
        while(True):
            sql = 'select rowid,last,time from %s where rowid > %s' % (trade_pair, row_id)
            result = self.db.execute(sql)
            data = result.fetchall()
            self.execute(data, pos)
            last_pair = data[-1]
            row_id = last_pair[0]
            if pos.ifStop():
                break
            # Waitting for next loop
            time.sleep(self.step * 10)

    def showData(self):
        sql = 'select rowid,last,time from eos_usdt'
        result = self.db.execute(sql)
        data = result.fetchall()
        for pair in data:
            self.x.append(pair[0])
            self.y.append(pair[1])
        poly = Polynomial(self.x, self.y)
        poly.fit()



if __name__ == '__main__':
    poly = Polynomial()
    poly.fit()
