# -*- coding:utf-8 -*-

import collections
import functools
import time


class RateLimiter(object):

    def __init__(self, max_calls, period=1.0, callback=None):
        self.calls = collections.deque()
        self.period = period
        self.max_calls = max_calls
        self.callback = callback
        self.exceed= False

    def __call__(self, f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            with self:
                if not self.exceed:
                    return f(*args, **kwargs)
                raise Exception("rate exceed")
        return wrapped

    def __enter__(self):
        
        if len(self.calls)>self.max_calls:
            while self._timespan >= self.callback:
                self.exceed=True
        else:
            self.exceed=False
            self.calls.append(time.time())
            print('max')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.calls.append(time.time())
        while self._timespan >= self.period:
            self.calls.popleft()

    @property
    def _timespan(self):
        return self.calls[-1] - self.calls[0]
