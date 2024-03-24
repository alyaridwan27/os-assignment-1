import threading
import random
from file_handler import write_to_all, write_to_even, write_to_odd

LOWER_NUM = 1
UPPER_NUM = 10000
BUFFER_SIZE = 100
MAX_COUNT = 10000

# Bounded buffer (stack) implementation
class BoundedBuffer:
    def __init__(self):
        self.buffer = []
        self.lock = threading.Lock()
        self.full = threading.Condition(self.lock)
        self.empty = threading.Condition(self.lock)

    def push(self, item):
        with self.full:
            while len(self.buffer) >= BUFFER_SIZE:
                self.full.wait()
            self.buffer.append(item)
            self.empty.notify()

    def pop(self):
        with self.empty:
            while not self.buffer:
                self.empty.wait()
            item = self.buffer.pop()
            self.full.notify()
            return item

# Producer function
def producer(buffer):
    for _ in range(MAX_COUNT):
        num = random.randint(LOWER_NUM, UPPER_NUM)
        buffer.push(num)
        write_to_all(num, "output/all.txt")

# Customer function
def customer(buffer, parity, write_function, filepath):
    while True:
        num = buffer.pop()
        if num % 2 == parity:
            write_function(num, filepath)
            break

if __name__ == "__main__":
    buffer = BoundedBuffer()

    producer_thread = threading.Thread(target=producer, args=(buffer,))
    customer1_thread = threading.Thread(target=customer, args=(buffer, 0, write_to_even, "output/even.txt"))
    customer2_thread = threading.Thread(target=customer, args=(buffer, 1, write_to_odd, "output/odd.txt"))

    producer_thread.start()
    customer1_thread.start()
    customer2_thread.start()

    producer_thread.join()
    customer1_thread.join()
    customer2_thread.join()

    print("Program executed successfully.")
