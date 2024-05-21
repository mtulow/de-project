# SuperFastPython.com
# example of one producer and one consumer with threads
from time import sleep
from random import random
from threading import Thread
from queue import Queue
 
# producer task
def producer_task(queue):
    print('Producer: Running')
    # generate items
    for i in range(10):
        # generate a value
        value = random()
        # block, to simulate effort
        sleep(value)
        # create a tuple
        item = (i, value)
        # add to the queue
        queue.put(item)
        # report progress
        print(f'>producer added {item}')
    # signal that there are no further items
    queue.put(None)
    print('Producer: Done')
 
# consumer task
def consumer_task(queue):
    print('Consumer: Running')
    # consume items
    while True:
        # get a unit of work
        item = queue.get()
        # check for stop
        if item is None:
            break
        # block, to simulate effort
        sleep(item[1])
        # report
        print(f'>consumer got {item}')
    # all done
    print('Consumer: Done')
 
def main():
    # create the shared queue
    queue = Queue()
    # start the consumer
    consumer = Thread(target=consumer_task, args=(queue,))
    consumer.start()
    # start the producer
    producer = Thread(target=producer_task, args=(queue,))
    producer.start()
    # wait for all threads to finish
    producer.join()
    consumer.join()

if __name__ == '__main__':
    print()
    main()
    print()