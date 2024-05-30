import os
import time
import json
import queue
import threading
import datetime as dt
from coinbase.websocket import (WSBase,
                                WSClient,
                                WSClientException,
                                WSClientConnectionClosedException,)


class TickerProducer(WSClient):
    def __init__(self, api_key, api_secret, buffer: queue.Queue):
        super().__init__(api_key, api_secret,
                         on_open=self.on_open,
                         on_message=self.on_message,
                         on_close=self.on_close)
        self.buffer = buffer

    def on_open(self):
        print("TickerProducer: Connection opened")

    def on_message(self, msg):
        print("TickerProducer: Message received")
        self.buffer.put(msg)
        print("TickerProducer: Message sent to buffer")

    def on_close(self):
        print("TickerProducer: Connection closed")
        self.buffer.put(None)


def consumer_task(buffer: queue.Queue):
    print('Consumer: Running')
    
    # consume items
    while True:
        # get a unit of work
        msg = buffer.get()
        # check for stop
        if msg is None:
            break
        # process the work
        msg_data = json.loads(msg)
        timestamp = dt.datetime.strptime(msg_data['timestamp'])
        print(msg_data)
        print(f'Consumer: Processed {msg}')

def producer_task(buffer: queue.Queue, identifier: int):
    print(f'Producer {identifier}: Running')
    # Generate items
    def on_open():
        print(f'Producer {identifier}: Connection opened')
        
    def on_message(msg):
        print(f'Producer {identifier}: Message received')
        buffer.put(msg)

    def on_close():
        print(f'Producer {identifier}: Connection closed')
        buffer.put(None)
        
    ws_client = WSClient(os.getenv('COINBASE_API_KEY'),
                         os.getenv('COINBASE_API_SECRET'),
                         on_open=on_open,
                         on_message=on_message,
                         on_close=on_close)

    try:
        ws_client.open()
        ws_client.subscribe(product_ids=["BTC-USD", "ETH-USD"], channels=["ticker",])
        ws_client.run_forever_with_exception_check()
    except WSClientConnectionClosedException as e:
        print("Connection closed! Retry attempts exhausted.")
    except WSClientException as e:
        print("Error encountered!")

def main():
    # Create the shared queue
    buffer = queue.Queue()

    # Start the consumer
    consumer = threading.Thread(target=consumer_task, args=(buffer,))
    consumer.start()

    # Start the producer
    producer = threading.Thread(target=producer_task, args=(buffer, 0))
    producer.start()

    # Wait for the producer to finish
    producer.join()
    
    # Wait for the consumer to finish
    consumer.join()

if __name__ == '__main__':
    print()
    main()
    print()