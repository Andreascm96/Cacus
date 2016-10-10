from datetime import datetime
from models import Trade, Session

class Portfolio(object):
    open_positions = []
    closed_positions = []
    P_L = 0
    PL_ratio = 0

    def __init__(self, starting_capital):
        self.capital = starting_capital
        self.account_value = starting_capital

    def open_position(self, enter_price):
        new_trade = Trade(enter_price=enter_price, time=datetime.now())
        session = Session()
        session.add(new_trade)
        session.commit()