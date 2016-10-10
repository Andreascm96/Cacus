from portfolio import Portfolio

class Executor(object):

    def __init__(self, portfolio):
        self.portfolio = portfolio

    def buy(self):
        pass

    def sell(self):
        pass

    def signal(self, signal, current_price):
        if signal == "BUY":
            print("Buying")
            self.portfolio.open_position(current_price)
        elif signal == "SELL":
            print("Selling")