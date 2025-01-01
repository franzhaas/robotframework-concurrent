from robotframework_concurrent import concurrent_keyword
import time


class concurrent_keyword_demo(concurrent_keyword.concurrent_keyword_execution_base):
    def __init__(self):
        super().__init__()

    @concurrent_keyword.make_function_concurrent
    def wait_and_trigger_event(self):
        time.sleep(2)
        self.run_keyword_concurrent("Log", "Triggering event", "INFO", False, True)
        time.sleep(1)
        self.run_keyword_concurrent("Log", "Triggering event", "INFO", False, True)
        
