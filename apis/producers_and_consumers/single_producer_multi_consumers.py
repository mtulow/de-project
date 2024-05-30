# example of one producer and multiple consumers with threads
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
    # signal that there are no further items
    queue.put(None)
    print('Producer: Done')
 
# consumer task
def consumer_task(queue, identifier):
    print(f'Consumer {identifier}: Running')
    # consume items
    while True:
        # get a unit of work
        item = queue.get()
        # check for stop
        if item is None:
            # add the signal back for other consumers
            queue.put(item)
            # stop running
            break
        # block, to simulate effort
        sleep(item[1])
        # report
        print(f'>consumer {identifier} got {item}')
    # all done
    print(f'Consumer {identifier}: Done')
 
def main():
    # create the shared queue
    queue = Queue()
    # start the consumers
    consumers = [Thread(target=consumer_task, args=(queue,i)) for i in range(3)]
    for consumer in consumers:
        consumer.start()
    # start the producer
    producer = Thread(target=producer_task, args=(queue,))
    producer.start()
    # wait for all threads to finish
    producer.join()
    for consumer in consumers:
        consumer.join()

if __name__ == '__main__':
    print()
    main()
    print()