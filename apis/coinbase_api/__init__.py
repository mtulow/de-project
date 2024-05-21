import os
import json
import threading
from coinbase.websocket import WSBase

class Consumer(threading.Thread):
    pass


class Producer(threading.Thread):
    def __init__(self,):
        threading.Thread.__init__(self)
        api_key = os.environ.get('COINBASE_API_KEY')
        api_secret = os.environ.get('COINBASE_API_SECRET')
        self.ws_client = WSBase(api_key, api_secret)
        self.producer_lock = threading.Lock()

    def on_open(self):
        print("Producer: Connection opened")
        
    def on_message(self, msg):
        print("Producer: Message received")
        self.producer_lock.acquire()
        
        self.producer_lock.release()

    def on_close(self):
        print("Producer: Connection closed")
        self.producer_lock.acquire()
        self.producer.close()
        self.producer_lock.release()

    def start(self):
        self.producer_lock.acquire()
        self.producer.start()
        self.producer_lock.release()

    def stop(self):
        self.producer_lock.acquire()
        self.producer.close()
        self.producer_lock.release()

    def is_open(self):
        return self.producer.is_open()

    def send(self, msg):
        self.producer_lock.acquire()
        self.producer.send(msg)
        self.producer_lock.release()