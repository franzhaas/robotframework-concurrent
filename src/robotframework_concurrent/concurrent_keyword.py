import robot.api.logger as logger
from queue import Queue
from queue import Empty
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
def make_function_concurrent(fun):
    """
    This decorator is used to make a method concurrent.
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

    def concurrent_fun(self, *args, **kwargs):
        self._2original_thread_queue.put(_concurrentEvent.START)
        return concurrent_keyword_execution_base._threadPool.submit(fun, self, *args, **kwargs)
    return concurrent_fun

class concurrent_keyword_execution_base:
    _threadPool = ThreadPoolExecutor(max_workers=os.cpu_count()*2)

    def __init__(self):
        self._2original_thread_queue = Queue()
        self._executions = 0

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
    def run_keyword_concurrent(self, keyword, *args, **kwargs):
        """
        This function is used to run a keyword from the originating thread.
        """
        if threading.current_thread() == threading.main_thread():
            _run_keyword(keyword, *args, **kwargs)
        else:
            self._2original_thread_queue.put((_concurrentEvent.CALL, _run_keyword, None, (keyword, *args,), kwargs,))

    def _work_message(self, timeout=None):
        msg = self._2original_thread_queue.get(timeout=timeout)
        match msg:
            case _concurrentEvent.START:
                self._executions += 1
            case _concurrentEvent.END:
                self._executions -= 1
            case (_concurrentEvent.EXCEPTION, e):
                self._executions -= 1
                logger.error(f"Exception in concurrent execution: {e}")
            case (_concurrentEvent.CALL, fun, None, args, kwargs):
                fun(*args, **kwargs)
            case (_concurrentEvent.CALL, fun, q, args, kwargs):
                q.put(fun(*args, **kwargs))
            case msg:
                raise AssertionError(f"Unexpected message from concurrent execution: '{msg}'")
        self._2original_thread_queue.task_done()
    
    def poll_messages_from_tasks(self):
        try:
            while True:
                self._work_message(timeout=0)
        except Empty:
            pass


    def wait_for_concurrent_execution_completion(self ):
        """
        This function is used to wait for the completion of all concurrent executions
        """
        while self._executions > 0 or not self._2original_thread_queue.empty():
            self._work_message()
