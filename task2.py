import time
import random
from typing import Callable


def speed_test(obj: object) -> object:
    def wrapper(func: Callable, counter: str) -> Callable:
        def inner(*args, **kwargs) -> None:
            t1 = time.time()
            func(*args, **kwargs)
            t2 = time.time()
            counter_value = getattr(obj, counter)
            counter_value += t2 - t1
            setattr(obj, counter, counter_value)
        return inner

    def del_obj(counters: list) -> object:
        def inner(self) -> object:
            for counter in counters:
                print(counter, getattr(self, counter))
            return obj
        return inner

    def wrap_obj() -> object:
        method_list = [fu for fu in dir(obj)
                       if callable(getattr(obj, fu))
                       and not fu.startswith('__')]
        counters_list = [str(method)+'_counter' for method in method_list]

        for pos, method in enumerate(method_list):
            attr = getattr(obj, method)
            setattr(obj, counters_list[pos], 0)
            setattr(obj, method, wrapper(attr, counters_list[pos]))
        setattr(obj, "__del__", del_obj(counters_list))

        return obj
    return wrap_obj()


@speed_test
class Closed(object):
    def m1(self, n) -> None:
        time.sleep(n)

    def m2(self, n) -> None:
        time.sleep(n)


def do_test(obj: Closed) -> None:
    for r in range(50):
        if random.random() > 0.5:
            obj.m1(random.random() * 0.3)
        else:
            obj.m2(random.random() * 0.1)


obj = Closed()
do_test(obj)
