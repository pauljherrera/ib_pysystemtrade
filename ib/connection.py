# -*- coding: utf-8 -*-

import numpy as np
import ib_insync as ib


def get_ib_connection(host='127.0.0.1', port=4002):
    """
    Returns a connection to Interactive Brokers.
    
    :param host: str. IP to stablish the connection with.
    :param port: int. Port number to stablish the connection with.
    
    :return: ib_insync.IB instance with a connection already stablished.
    """
    client_id = np.random.randint(1, 9999)
    ib_connection = ib.IB()
    ib_connection.connect(host, port, clientId=client_id)
    
    return ib_connection


class IBConnection:
    """
    Simple class that will be inherited by those components that need
    to use a unique or shared connection with Interactive Brokers.
    """
    def __init__(self, ib_connection=None):
        """
        :param ib_connection (optional): ib_insync.IB instance with a 
               connection already stablished. If None is passed, will 
               automatically create a new connection.
        """
        # Connecting to IB.
        if ib_connection:
            self.ib = ib_connection
        else:
            self.ib = get_ib_connection()
            

if __name__ == "__main__":
    connection = IBConnection()
    
    
    