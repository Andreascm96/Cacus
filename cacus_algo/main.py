import settings
import prices
import datetime
import threading
import Queue
import signal
import sys
import time

from events import TickEvent
from analysis import Analyzer
from executor import Executor
from market import Market
from portfolio import Portfolio

class StoppableThread(threading.Thread):
    def __init__(self):
        super(StoppableThread, self).__init__()
        self._stop = threading.Event()

    def stop(self):
        print("Stopping")
        self._stop.set()

class TradingThread(StoppableThread):
    def __init__(self, queue, analyzer, events):
        super(TradingThread, self).__init__()
        self.queue = queue
        self.analyzer = analyzer
        self.events = events

    def run(self):
        while not self._stop.isSet():
            print("Trading")
            time.sleep(settings.HEARTBEAT)

class MarketThread(StoppableThread):
    def __init__(self, market):
        super(MarketThread, self).__init__()
        self.market = market

    def run(self):
        while not self._stop.isSet():
            time.sleep(settings.HEARTBEAT)
            self.market.update()

if __name__ == "__main__":
    q = Queue.Queue()

    p = Portfolio(20000)
    e = Executor(p)
    a = Analyzer(portfolio=p)
    m = Market(queue=q)

    trading_thread = TradingThread(queue=q, analyzer=a, events=e)
    market_thread = MarketThread(market=m)

    def receive_signal(signum, stack):
        print("You quit")
        trading_thread.stop()
        market_thread.stop()
        sys.exit(0)

    market_thread.start()
    trading_thread.start()
    signal.signal(signal.SIGINT, receive_signal)
