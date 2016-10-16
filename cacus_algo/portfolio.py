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

    @property
    def has_open_position(self):
        return len(self.open_position) > 0

    def calculate_profit_loss(self, ticker):
        session = Session()
        trades = session.query(Trade).filter(ticker==ticker, open==True)

    def open_position(self, enter_price):
        new_trade = Trade(enter_price=enter_price, time=datetime.now())
        session = Session()
        session.add(new_trade)
        session.commit()

    def close_position(self, current_price):
        open_trade = session.query(Trade).first()
        open_trade.closed = True
        open_trade.profit_loss = current_price - open_trade.enter_price
        open_trade.exit_price = current_price
        open_trade.commit()