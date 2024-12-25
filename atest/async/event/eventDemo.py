from robotframework_concurrent import async_execution_keyword
import time


class eventDemo(async_execution_keyword.async_keyword_execution_base):
    def __init__(self):
        super().__init__()

    @async_execution_keyword.make_function_async
    def wait_and_trigger_event(self):
        time.sleep(1)
        self.run_keyword_async("Log", "Triggering event", "INFO", False, True)
        time.sleep(1)
