import math
import json
import csv

from queue_class import QueuingClass
from cacus_algo import settings
from models import Session, Quote
from sqlalchemy import desc
from datetime import datetime, timedelta

class Analyzer(object):
    bollinger_bands = None
    RSI = None
    golden_cross = None
    enough_data = False

    def __init__(self, portfolio):
        self.portfolio = portfolio

    class BollingerBands(object):
        upper_band = None
        lower_band = None

        def __init__(self, prices):
            self._prices = prices
            self.n = 20
            self.n_stddevs = 2
            self._calc_limits()

        def _calc_limits(self):
            avg = (sum(self._prices)*1.0)/len(self._prices)
            variance = sum([(price - avg)**2 for price in self._prices])/len(self._prices)
            stDev = math.sqrt(variance)
            last_close_price = self._prices[0]
            self.upper_band = avg + stDev * self.n_stddevs
            self.lower_band = avg - stDev * self.n_stddevs

    def get_n_last_prices(self, n):
        session = Session()
        l = session.query(Quote.price).order_by(desc(Quote.time)).limit(n).all()
        return [n[0] for n in l]

    def get_last_price(self):
        session = Session()
        price = session.query(Quote.price).first()[0]
        print(price)
        return price

    def smooth_average(self, l, alpha):
        if not l:
            return 0
        yt_prev = l[0]
        for yt in l[1:]:
            yt_prev = alpha*yt+(1-alpha)*yt_prev
        return yt_prev

    def calculate_RSI(self, historical_close_prices):
        U = []
        D = []

        prev_close = historical_close_prices[0]
        for tick in historical_close_prices[1:]:
            if tick < prev_close:
                D.append(prev_close - tick)
            else:
                U.append(tick - prev_close)
            prev_close = tick

        # Smooth the average
        SMMA_U = 0
        SMMA_D = 0
        alpha = 1.0/len(historical_close_prices)
        
        # Smooth up closes
        SMMA_U = self.smooth_average(U, alpha)

        # Smooth down closes
        SMMA_D = self.smooth_average(D, alpha)

        # Calculate RSI
        try:
            RS = SMMA_U/SMMA_D
            RSI = 100-(100/(1+RS))
        except ZeroDivisionError:
            RSI = 100

        return RSI

    def generate_signal(self, quote):
        current_price = quote.price
        last_20_prices = self.get_n_last_prices(21)[1:]
        last_14_prices = self.get_n_last_prices(15)[1:]
        last_15_prices = self.get_n_last_prices(16)[1:]
        last_50_prices = self.get_n_last_prices(51)[1:]

        RSI = self.calculate_RSI(last_14_prices)
        bollinger_bands = self.BollingerBands(last_20_prices)
        golden_cross = self.golden_cross(last_50_prices, last_15_prices)
        print("Current price: " + str(current_price))
        print("RSI: " + str(RSI))
        print("Bollinger bands upper: " + str(bollinger_bands.upper_band))
        print("Bollinger bands lower: " + str(bollinger_bands.lower_band))
        print("Golden cross: " + str(golden_cross))
        signal = "STAND ASIDE"

        if RSI > 70 and current_price > bollinger_bands.upper_band and golden_cross:
            signal = "SELL"
        elif RSI < 70 and current_price < bollinger_bands.lower_band and golden_cross:
            signal = "BUY"

        print("Advice: " + str(signal))
        print("\n")

        return signal

    def golden_cross(self, long_run_prices, short_run_prices):
        long_run_avg = (sum(long_run_prices)*1.0)/len(long_run_prices)
        short_run_avg = (sum(short_run_prices)*1.0)/len(short_run_prices)
        return short_run_avg > long_run_avg
        

def get_signal(current_price, bollingers):
    upper_band = bollingers.upper_band
    lower_band = bollingers.lower_band
    if current_price < lower_band:
        return "BUY"
    elif current_price > upper_band:
        return "SELL"
    else:
        return "HOLD"