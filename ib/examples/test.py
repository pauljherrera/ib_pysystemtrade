import ib_insync as ib

client = ib.IB()
client.connect('127.0.0.1', 4002, clientId=10)

contract = ib.Forex('EURUSD')
client.qualifyContracts(contract)

order = ib.MarketOrder('BUY', 69385, account=client.managedAccounts()[0])
trade = client.placeOrder(contract, order)
while not trade.isDone():
    client.waitOnUpdate()



