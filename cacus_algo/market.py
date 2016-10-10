import requests

from datetime import datetime

from models import Session, Quote
from analysis import Analyzer

class Market(object):
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def update(self):
        url = "http://download.finance.yahoo.com/d/quotes.csv?s=^GDAXI&f=nsl1opc1p2&e=.csv"
        r = requests.get(url)
        content = r.text.split(',')
        price = content[2]

        new_quote = Quote(price=price, time=datetime.now())
        session = Session()
        session.add(new_quote)
        session.commit()

        self.analyzer.notify()