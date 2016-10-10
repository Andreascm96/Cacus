import settings
import prices
import models
import datetime
import time

from analysis import Analyzer
from executor import Executor
from market import Market
from portfolio import Portfolio


if __name__ == "__main__":
    p = Portfolio(20000)
    e = Executor(p)
    a = Analyzer(e)
    m = Market(analyzer=a)

    while True:
        m.update()
        time.sleep(settings.HEARTBEAT)