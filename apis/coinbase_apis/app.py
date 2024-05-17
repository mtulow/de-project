import os
import time
from pprint import pprint
from dotenv import load_dotenv
from coinbase.websocket import (WSClient, WSClientConnectionClosedException,
                                WSClientException)

def on_open():
    print("Connection opened!")
    print()

def on_message(message):
    print()
    pprint(message, indent=4)

def on_close():
    print()
    print("Connection closed!")
    

load_dotenv()

api_key = os.getenv("COINBASE_API_KEY")
api_secret = os.getenv("COINBASE_API_SECRET")


def main():
    # create a websocket client
    client = WSClient(api_key=api_key,
                      api_secret=api_secret,
                      on_open=on_open,
                      on_message=on_message,
                      on_close=on_close,)

    # Run the client in a try-except block to handle exceptions
    try:
        client.open()
        client.subscribe(product_ids=["BTC-USD", "ETH-USD"], channels=["ticker",])
        client.run_forever_with_exception_check()
    except WSClientConnectionClosedException as e:
        print("Connection closed! Retry attempts exhausted.")
    except WSClientException as e:
        print("Error encountered!")



if __name__ == "__main__":
    print()
    main()
    print()