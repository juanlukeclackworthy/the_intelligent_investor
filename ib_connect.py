from ib_insync import IB

def connect_ib(client_id=1, port=7497):
    ib = IB()
    ib.connect('127.0.0.1', port, clientId=client_id)
    return ib