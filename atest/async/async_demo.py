import asyncio
from robot.api.deco import keyword
import robot.libraries.BuiltIn as BuiltIn
from robot.api import logger
import logging
import threading


class async_demo():
    def __init__(self):
        super().__init__()
        BuiltIn.BuiltIn().run_keyword("Log", f"loading  {threading.current_thread().ident} this call is for __init__ of the async_demo", "INFO")
        self._task = []
    
    async def _task_async(self):
        await asyncio.sleep(1)
        BuiltIn.BuiltIn().run_keyword("Log", f"Slept first 1s  {threading.current_thread().ident}", "INFO")
        await asyncio.sleep(2)
        logger.info(f"Slept second 2s {threading.current_thread().ident}")
        logging.info("logging from python")
        print("*INFO* print from python")

    @keyword
    async def  start_async_wait(self):
        self._task.append(asyncio.create_task(self._task_async()))

    @keyword
    async def  start_async_wait_with_return(self):
        await asyncio.sleep(1)
        return 1

    @keyword
    async def wait_for_events(self):
        while self._task:
            await self._task.pop()
