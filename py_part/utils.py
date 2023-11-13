import sys
import threading
import time


class Timing(object):
    def __init__(self, f):
        self.f = f
        self.active = False

    def __call__(self, *args):
        if self.active:
            return self.f(*args)
        start = time.time()
        self.active = True
        res = self.f(*args)
        end = time.time()
        self.active = False
        print(f'func \'{self.f.__name__}\' done by {(end - start):.5f} s')
        return res


class MyThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._result = None

    def run(self):
        if self._target is None:
            return
        try:
            self._result = self._target(*self._args, **self._kwargs)
        except Exception as e:
            print(f"{type(e).__name__}: {e}", file=sys.stderr)

    def join(self, *args, **kwargs):
        super().join(*args, **kwargs)
        return self._result
