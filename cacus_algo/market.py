import requests

from queue_class import QueuingClass
from datetime import datetime
from events import TickEvent
from models import Session, Quote
from analysis import Analyzer

class Market(object):
    def __init__(self, queue):
        self.queue = queue

    def update(self):
        url = "http://download.finance.yahoo.com/d/quotes.csv?s=^GDAXI&f=nsl1opc1p2&e=.csv"
        r = requests.get(url)
        content = r.text.split(',')
        price = content[2]

        ticker = "DAX"

        new_quote = Quote(price=price, ticker=ticker, time=datetime.now())
        session = Session()
        session.add(new_quote)
        session.commit()

        tick_event = TickEvent(ticker=ticker, price=price)
        
        self.queue.put(tick_event)