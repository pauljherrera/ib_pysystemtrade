import ib_insync as ib

client = ib.IB()
client.connect('127.0.0.1', 4002, clientId=10)

print(client.portfolio())