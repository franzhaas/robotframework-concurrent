from robot.api import logger
from robotframework_concurrent import concurrent_keyword
import time


def _is_even(nr: int) -> bool:
    if nr == 0:
        return True
    rVal = True
    while nr:
        nr -= 1
        rVal = (not rVal)
    return rVal

def _is_odd(nr: int):
    if nr == 0:
        return False
    return _is_even(nr-1)


class evenOrOdd(concurrent_keyword.concurrent_keyword_execution_base):
    def __init__(self):
        super().__init__()

    @concurrent_keyword.make_function_concurrent
    def odd(self, nr: int):
        rVal = _is_odd(int(nr))
        self.call_function_from_originating_thread(logger.warn, f"{nr} odd is {rVal}")
        return rVal
    
    def even(self, nr: int):
        rVal = self.odd(nr-1)
        self.call_function_from_originating_thread(logger.warn, f"starting even check")
        return rVal