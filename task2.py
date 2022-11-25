import time
import random
from collections import defaultdict
from typing import Callable

methods = defaultdict(float)


def add_time_tracker(func: type) -> Callable:
    """
    Covers method (e.g. class method) and count time of exec
    :param func: e.g. <function Closed.m1 at 0x102be0670>
    :return:
    """

    def wrapper(*args, **kwargs) -> None:
        t1 = time.time()
        func(*args, **kwargs)
        t2 = time.time()
        res = t2 - t1
        methods[func] += res

    return wrapper


def funcs_tracker(extra_functionality: Callable) -> Callable:
    """
    Covers a class to expand its functionality but not to modify the class
    :param extra_functionality: tuple of decorators
    :return: a new instance of a class with expanded functionality
    """
    def inner(obj: type) -> Callable:
        def wrapper(*args, **kwargs) -> Callable:
            method_list = [func for func in dir(obj)
                           if callable(getattr(obj, func))
                           and not func.startswith('__')]
            for method in method_list:
                attr = getattr(obj, method)
                setattr(obj, method, extra_functionality(attr))
            return obj(*args, **kwargs)
        return wrapper
    return inner


def get_methods_items(func: type) -> Callable:
    """
    Stdout items of 'methods' dictionary
    :param func:
    :return: None
    """
    def wrapper(*args, **kwargs) -> None:
        func(*args, **kwargs)
        for k, v in methods.items():
            method_name = str(k).split()[1]
            method_value = round(float(v), 2)
            print("{}: {}".format(method_name, method_value))
    return wrapper


@funcs_tracker(extra_functionality=add_time_tracker)
class Closed(object):
    def m1(self, n) -> None:
        time.sleep(n)

    def m2(self, n) -> None:
        time.sleep(n)


@get_methods_items
def do_test(obj: Closed) -> None:
    for r in range(50):
        if random.random() > 0.5:
            obj.m1(random.random() * 0.1)
        else:
            obj.m2(random.random() * 0.1)


obj = Closed()
do_test(obj)

# Closed.m2: 1.58
# Closed.m1: 1.42
