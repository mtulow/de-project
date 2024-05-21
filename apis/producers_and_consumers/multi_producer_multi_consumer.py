# SuperFastPython.com
# example of multiple producers and multiple consumers with threads
import os
import boto3
import datetime as dt
from time import sleep
from random import random
from threading import Thread
from threading import Barrier
from queue import Queue
from coinbase.websocket import (WSBase, WSClient,
                                WSClientException,
                                WSClientConnectionClosedException,)

 
# producer task
def producer_task(barrier, buffer, identifier):
    print(f'Producer {identifier}: Running')

    def on_open():
        print(f'Producer {identifier}: Connection opened')

    def on_message(msg):
        print(f'Producer {identifier}: Message received')
        now = dt.datetime.now()
        filename = f"ticker_{now.strftime('%Y%m%d_%I%M%S')}.json"
        subdir = now.strftime('crypto_market/%Y/%m/%d/%H/%M')
        data = dict(filename=filename,
                    subdir=subdir,
                    message=msg)
        buffer.put(data)

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
    finally:
        ws_client.close()
        print(f'Producer {identifier}: Done')

    
# consumer task
def consumer_task(buffer, identifier):
    print(f'Consumer {identifier}: Running')

    def write_to_local(filename: str, message: dict):
        with open(filename, 'w') as file:
            file.write(message)

    def write_to_s3(
            filename: str,
            key: str,
            bucket_name: str = 'economic-finance-20240517094908322100000001'
        ):
        s3_client = boto3.client('s3')
        s3_client.upload_file(filename,
                              bucket=bucket_name,
                              key=key,)

    # consume items
    while True:
        # get a unit of work
        item = buffer.get()
        # check for stop
        if item is None:
            # add the signal back for other consumers
            buffer.put(item)
            # stop running
            break
        # Get the filename and sub-directory
        write_to_local(item['filename'], item['message'])
        # write to S3
        write_to_s3(item['filename'], item['subdir'])
    # all done
    print(f'Consumer {identifier}: Done')

def main():   
    # create the shared buffer
    queue = Queue()
    # create the shared barrier
    n_producers = 2
    barrier = Barrier(n_producers)
    # start the consumers
    consumers = [Thread(target=consumer_task, args=(queue,i)) for i in range(2)]
    for consumer in consumers:
        consumer.start()
    # start the producers
    producers = [Thread(target=producer_task, args=(barrier,queue,i)) for i in range(n_producers)]
    # start the producers
    for producer in producers:
        producer.start()
    # wait for all threads to finish
    for producer in producers:
        producer.join()
    for consumer in consumers:
        consumer.join()

if __name__ == '__main__':
    print()
    main()
    print()