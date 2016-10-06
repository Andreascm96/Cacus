import math
import requests
import json
import csv

from datetime import datetime, timedelta

class BollingerBands(object):
    upper_band = None
    lower_band = None

    def __init__(self, prices, n_days, n_stddevs):
        self._prices = prices
        self.n_days = n_days
        self.n_stddevs = n_stddevs
        self._calc_limits()

    def _calc_limits(self):
        avg = sum(prices)/len(prices)
        variance = sum([(price - avg)**2 for price in self._prices])/len(prices)
        stDev = math.sqrt(variance)
        last_close_price = self._prices[0]
        self.upper_band = avg + stDev * self.n_stddevs
        self.lower_band = avg - stDev * self.n_stddevs

#historical = json.loads('{"data":[{"date":"2016-10-05","value":10585.780273},{"date":"2016-10-04","value":10619.610352},{"date":"2016-09-30","value":10511.019531},{"date":"2016-09-29","value":10405.540039},{"date":"2016-09-28","value":10438.339844},{"date":"2016-09-27","value":10361.480469},{"date":"2016-09-26","value":10393.709961}],"identifier":"$DAX","item":"close_price","result_count":7,"page_size":50000,"current_page":1,"total_pages":1,"api_call_credits":1}')['data']

historical = []
with open('csv.csv', 'r') as f:
    reader = csv.reader(f, delimiter=',', quotechar='"')
    for n in range(17):
        reader.next()

    for l in reader:
        prices = l[0]
        prices_as_a_list = prices.split(';')
        close_price = float(prices_as_a_list[1])
        historical.append(close_price)

def smooth_average(l, alpha):
    yt_prev = l[0]
    for yt in l[1:]:
        yt_prev = alpha*yt+(1-alpha)*yt_prev
    return yt_prev

def calculate_RSI(historical_close_prices):
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
    SMMA_U = smooth_average(U, alpha)

    # Smooth down closes
    SMMA_D = smooth_average(D, alpha)

    # Calculate RSI
    RS = SMMA_U/SMMA_D

    try:
        RSI = 100-(100/(1+RS))
    except ZeroDivisionError:
        RSI = 100

    return RSI

print(calculate_RSI(historical))

def get_signal(current_price, bollingers):
    upper_band = bollingers.upper_band
    lower_band = bollingers.lower_band
    if current_price < lower_band:
        return "BUY"
    elif current_price > upper_band:
        return "SELL"
    else:
        return "HOLD"