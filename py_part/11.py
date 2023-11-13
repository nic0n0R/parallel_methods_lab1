import random
import threading
import time


MAX_CUSTOMERS = 5
MAX_CHAIRS = 3

barber_semaphore = threading.Semaphore(0)
customer_semaphore = threading.Semaphore(0)
mutex = threading.Semaphore(1)

waiting_customers = []

def barber():
    while True:
        print("Барбер спит...")
        barber_semaphore.acquire()
        mutex.acquire()
        if len(waiting_customers) > 0:
            customer = waiting_customers.pop(0)
            print(f"Барбер стрижет клиента {customer}")
            mutex.release()
            time.sleep(random.randint(1, 5))
            print(f"Барбер закончил стричь клиента {customer}")
            customer_semaphore.release()
        else:
            mutex.release()


def customer(index):
    global waiting_customers
    time.sleep(random.randint(1, 5))
    mutex.acquire()
    if len(waiting_customers) < MAX_CHAIRS:
        waiting_customers.append(index)
        print(f"Клиент {index} ждет...")
        mutex.release()
        barber_semaphore.release()
        customer_semaphore.acquire()
        print(f"Клиент {index} закончил стричься")
    else:
        print(f"Клиент {index} уходит, потому что комната ожидания заполнена")
        mutex.release()


def main():
    barber_thread = threading.Thread(target=barber)
    customer_threads = [threading.Thread(target=customer, args=(i,)) for i in range(MAX_CUSTOMERS)]

    barber_thread.start()
    for t in customer_threads:
        t.start()


if __name__ == '__main__':
    main()
