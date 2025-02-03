import random
import collections


def calc_pi():
    n = 1000000
    count = 0
    for _ in range(n):
        count += int(random.random() ** 2 + random.random() ** 2 <= 1)
        yield
    print(f"pi is {4 * count / n}")

def calc_e():
    e = d = 1
    for i in range(1, 1000000):
        d /= i
        e += d
        yield
    print(f"e is {e}")

tasks = collections.deque([calc_pi(), calc_e()])

while tasks:
    item = tasks.pop()
    try:
        next(item)
        tasks.appendleft(item)
    except StopIteration:
        pass


