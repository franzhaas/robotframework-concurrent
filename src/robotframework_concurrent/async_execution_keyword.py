import robot.api.logger as logger
from queue import Queue
from robot.api.deco import not_keyword
import threading
from enum import Enum as Enum
from concurrent.futures import ThreadPoolExecutor
import os
import robot.libraries.BuiltIn as BuiltIn

class _concurrentEvent(Enum):
    START = 1
    END = 2
    CALL = 3
    EXCEPTION = 4


def _run_keyword(keyword, *args, **kwargs):
    return BuiltIn.BuiltIn().run_keyword(keyword, *args)

@not_keyword
def make_function_async(fun):
    """
    This decorator is used to make a method asynchronous.
    """

    def _wrap(fun):
        def _wrapped(obj, *args, **kwargs):
            try:
                rval = fun(obj, *args, **kwargs)
                obj._2original_thread_queue.put(_concurrentEvent.END)
                return rval
            except Exception as e:
                obj._2original_thread_queue.put((_concurrentEvent.EXCEPTION, e,))
                raise e
        return _wrapped

    fun = _wrap(fun)

    def async_fun(self, *args, **kwargs):
        self._2original_thread_queue.put(_concurrentEvent.START)
        return async_keyword_execution_base._threadPool.submit(fun, self, *args, **kwargs)

    return async_fun

class async_keyword_execution_base:
    _threadPool = ThreadPoolExecutor(max_workers=os.cpu_count()*2)

    def __init__(self):
        self._2original_thread_queue = Queue()
    
    @not_keyword
    def call_function_from_originating_thread(self, fun, *args, **kwargs):
        """
        This function is used to call a function from the originating thread, ignoring the result.
        """
        if threading.current_thread() == threading.main_thread():
            fun(*args, **kwargs)
        else:
            self._2original_thread_queue.put((_concurrentEvent.CALL, fun, None, args, kwargs,))
    
    
    @not_keyword
    def call_function_from_originating_thread_and_wait_for_result(self, fun, *args, **kwargs):
        """
        This function is used to call a function from the originating thread and wait for the result.
        """
        if threading.current_thread() == threading.main_thread():
            return fun(*args, **kwargs)
        else:
            _q = Queue()
            self._2original_thread_queue.put((_concurrentEvent.CALL, fun, _q,   args, kwargs,))
            return _q.get()
        
    @not_keyword
    def run_keyword_async(self, keyword, *args, **kwargs):
        """
        This function is used to run a keyword from the originating thread.
        """
        if threading.current_thread() == threading.main_thread():
            return _run_keyword(*args, **kwargs)
        else:
            self._2original_thread_queue.put((_concurrentEvent.CALL, _run_keyword, None, (keyword, *args,), kwargs,))
            
    def wait_for_async_execution_completion(self ):
        """
        This function is used to wait for the completion of all asynchronous executions
        """
        firstMessage = self._2original_thread_queue.get()
        assert firstMessage == _concurrentEvent.START, "Expected start, received: {firstMessage}"
        _executions = 1
        self._2original_thread_queue.task_done()
        while _executions > 0:
            msg = self._2original_thread_queue.get()
            match msg:
                case _concurrentEvent.START:
                    _executions += 1
                case _concurrentEvent.END:
                    _executions -= 1
                case (_concurrentEvent.EXCEPTION, e):
                    _executions -= 1
                    logger.error(f"Exception in asynchronous execution: {e}")
                case (_concurrentEvent.CALL, fun, None, args, kwargs):
                    fun(*args, **kwargs)
                case (_concurrentEvent.CALL, fun, q, args, kwargs):
                    q.put(fun(*args, **kwargs))
            self._2original_thread_queue.task_done()
