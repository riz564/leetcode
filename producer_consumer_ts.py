import threading
from queue import Queue
import time

NUM_PRODUCERS = 2
NUM_CONSUMERS = 3
QUEUE_CAPACITY = 10
SENTINEL = object()  # unique stop marker

q = Queue(maxsize=QUEUE_CAPACITY)

def producer(pid: int, items: int):
    for i in range(items):
        item = (pid, i)
        q.put(item)  # blocks if full (backpressure)
        print(f"[P{pid}] produced {item} | qsize={q.qsize()}")
        time.sleep(0.1)  # simulate work

def consumer(cid: int):
    while True:
        item = q.get()  # blocks if empty
        try:
            if item is SENTINEL:
                print(f"[C{cid}] stopping.")
                break
            # process
            time.sleep(0.15)  # simulate work
            print(f"[C{cid}] consumed {item} | qsize={q.qsize()}")
        finally:
            q.task_done()

def main():
    total_items_per_producer = 2

    # start consumers (non-daemon so we can join after sentinel)
    consumers = [threading.Thread(target=consumer, args=(c,)) for c in range(NUM_CONSUMERS)]
    for t in consumers:
        t.start()

    # start producers
    producers = [threading.Thread(target=producer, args=(p, total_items_per_producer)) for p in range(NUM_PRODUCERS)]
    for t in producers:
        t.start()

    # wait producers to finish
    for t in producers:
        t.join()

    # send one sentinel per consumer
    for _ in range(NUM_CONSUMERS):
        q.put(SENTINEL)

    # wait until all items (including sentinels) are processed
    q.join()

    # wait consumers to exit
    for t in consumers:
        t.join()

if __name__ == "__main__":
    main()
