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
            # попытка взять вилку слева
            # Если blocking установлен в True, то поток будет ждать, пока блокировка станет доступной.
            # Если blocking установлен в False, то поток вернет None, если блокировка уже захвачена другим потоком.
            if self.left_fork.acquire(blocking=True):
                # попытка взять вилку справа
                if self.right_fork.acquire(blocking=True):
                    # есть
                    print(f"{self.name} ест двумя вилками.")
                    # Ест две секунды
                    time.sleep(random.randint(1, 5))
                    # отложить вилки
                    self.right_fork.release()
                    self.left_fork.release()
                else:
                    # Не удалось взять вилку справа, отложить вилку слева
                    self.left_fork.release()


if __name__ == '__main__':
    forks = [threading.Lock() for _ in range(5)]

    # пять философов
    philosophers = [Philosopher(name=f"Философ {x}",
                                left_fork=forks[x],
                                right_fork=forks[(x + 1) % 5]) for x in range(5)]
    for philosopher in philosophers:
        philosopher.start()
