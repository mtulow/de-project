import os
import boto3
import datetime as dt
from queue import Queue
from threading import Thread, Barrier
# from coinbase_api import Producer, Consumer
from coinbase.websocket import WSBase, WSClient, WSClientException, WSClientConnectionClosedException



