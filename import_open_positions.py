import ibapi
from ibapi.client import EClient
from ibapi.wrapper import EWrapper

class IBWrapper(EWrapper):
    # Implementation of required functions goes here
    print("hello")

class IBClient(EClient):
    # Implementation of required functions goes here
    print("hello")

def main():
    # Create an instance of the IBWrapper and IBClient classes
    wrapper = IBWrapper()
    client = IBClient(wrapper)

    # Connect to the API
    client.connect('127.0.0.1', 7496, clientId='U9454063')

    # Log in to your account
    client.login('buckethead69', 'Iomenefrego69$')

    # Request a list of your open positions
    client.reqPositions()

    # Disconnect from the API
    client.disconnect()

if __name__ == '__main__':
    main()
