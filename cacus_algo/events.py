class Event(object):
    pass

class TickEvent(Event):
    event_type = "TICK"
    
    def __init__(self, ticker, price):
        self.ticker = ticker
        self.price = price

class ExecuteEvent(Event):
    event_type = "EXECUTE"

    def __init__(self, signal):
        self.signal = "BUY"