from ibapi import wrapper
from ibapi.client import EClient
from ibapi import contract



def printinstance(inst:object):
    attrs = vars(inst)
    print(', '.join("%s: %s" % item for item in attrs.items()))



class TestWrapper(wrapper.EWrapper):
	def connectAck(self):
		print("\nConnected.")




class TestClient(EClient):
	def __init__(self, wrapper):
		EClient.__init__(self, wrapper)



class TestApp(TestWrapper, TestClient):
	def __init__(self):
		TestWrapper.__init__(self)
		TestClient.__init__(self, wrapper=self)
        
	def contractDetails(self, reqID: int, 
      						 contractDetails: contract.ContractDetails):
		super().contractDetails(reqID, contractDetails)
		printinstance(contractDetails.summary)

	def contractDetailsEnd(self, reqID: int):
		super().contractDetailsEnd(reqID)
		print("contractDetailsEnd. ", reqID, "\n")



if __name__ == '__main__':
    app = TestApp()
    app.connect('127.0.0.1', 4002, clientId=0)

    # New contract.
    contract = contract.Contract()
    contract.secType = "NEWS"
    contract.exchange = "BT"

    app.reqContractDetails(213, contract)
    
    
    

