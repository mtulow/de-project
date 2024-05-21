import os
import boto3
from queue import Queue
from threading import Thread, Barrier
# from coinbase_api import Producer, Consumer
from coinbase.websocket import WSBase, WSClient, WSClientException, WSClientConnectionClosedException


def producer(barrier: Barrier, buffer: Queue, identifier: int):
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
    
    
def consumer(buffer: Queue):
    print('Consumer: Running')
    
    # consume items
    while True:
        # get a unit of work
        msg = buffer.get()
        # check for stop
        if msg is None:
            break
        # process the work
        s3_client = boto3.client('s3')
        s3_client.upload_file()
        # report
        print(f'Consumer: Processed {msg}')
        

def main():
    # create the shared queue
    buffer = Queue()
    # create the shared barrier
    n_producers = 3
    barrier = Barrier(n_producers)
    # start the consumer
    consumer = Thread(target=consumer, args=(buffer,))
    consumer.start()
    # start the producers
    producers = [Thread(target=producer, args=(barrier,buffer,i)) for i in range(n_producers)]
    # start the producers
    for producer in producers:
        producer.start()
    # wait for all threads to finish
    for producer in producers:
        producer.join()
    consumer.join()

if __name__ == '__main__':
    print()
    main()
    print()