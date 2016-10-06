from time import sleep

from ib.ext.Contract import Contract
from ib.ext.Order import Order
from ib.opt import Connection, message  

def error_handler(msg):
    print("Server Error : {message}".format(message=msg))

def reply_handler(msg):
    print("Server Response {type} {message}".format(type=msg.typeName, message=msg))

def historical_data_handler(msg):
    print("Hello world", msg)

def create_contract(symbol, sec_type, exch, prim_exch, curr):
    contract = Contract()
    contract.m_symbol = symbol
    contract.m_secType = sec_type
    contract.m_exchange = exch
    contract.m_primaryExch = prim_exch
    contract.m_currency = curr
    return contract

def create_order(order_type, quantity, action):
    order = Order()
    order.m_orderType = order_type
    order.m_totalQuantity = quantity
    order.m_action = action
    return order

def execDetails(msg):
    print('ID',msg.execution.m_execId,'PRICE',msg.execution.m_price)


if __name__ == "__main__":
    # Connect to the Trader Workstation (TWS) running on the
    # usual port of 7496, with a clientId of 100
    # (The clientId is chosen by us and we will need 
    # separate IDs for both the execution connection and
    # market data connection)
    tws_conn = Connection.create(port=7497, clientId=100)
    tws_conn.register(error_handler, 'Error')
    tws_conn.register(historical_data_handler, message.historicalData)
    tws_conn.register(execDetails, message.execDetails)
    tws_conn.connect()

    # Assign all of the server reply messages to the
    # reply_handler function defined above
    tws_conn.registerAll(reply_handler)

    # Create an order ID which is 'global' for this session. This
    # will need incrementing once new orders are submitted.
    order_id = 2

    # Create a contract in GOOG stock via SMART order routing
    goog_contract = create_contract('GOOG', 'STK', 'SMART', 'SMART', 'USD')
    while True:
        tws_conn.reqMktData(1,goog_contract,"",False)
        sleep(10)

    # Go long 100 shares of Google
    goog_order = create_order('MKT', 1, 'SELL')

    # Use the connection to the send the order to IB
    tws_conn.placeOrder(order_id, goog_contract, goog_order)

    # Disconnect from TWS
    tws_conn.disconnect()
