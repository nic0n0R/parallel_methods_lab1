import random
import threading
import time


class Philosopher(threading.Thread):

    def __init__(self, name, left_fork, right_fork):
        super().__init__(name=name)
        self.left_fork = left_fork
        self.right_fork = right_fork

    def run(self):
        while True:
            # Захватываем блокировки
            self.left_fork.acquire()
            self.right_fork.acquire()

            # Есть
            print(f"{self.name} ест")
            time.sleep(random.random())

            # Отпускаем блокировки
            self.right_fork.release()
            self.left_fork.release()


if __name__ == "__main__":
    # Создаем пять вилок
    forks = [threading.Lock() for _ in range(5)]

    # Создаем пять философов
    philosophers = [Philosopher(name=f"Философ {i}", left_fork=forks[i], right_fork=forks[(i + 1) % 5]) for i in range(5)]

    # Запускаем философов
    for philosopher in philosophers:
        philosopher.start()
