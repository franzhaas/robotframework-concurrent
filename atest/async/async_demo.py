import asyncio
from robot.api.deco import keyword
import robot.libraries.BuiltIn as BuiltIn


class async_demo():
    def __init__(self):
        super().__init__()
    
    async def _task_async(self):
        await asyncio.sleep(1)
        BuiltIn.BuiltIn().run_keyword("Log", "Slept first 1s", "INFO")
        await asyncio.sleep(2)
        BuiltIn.BuiltIn().run_keyword("Log", "Slept second 2s", "INFO")

    @keyword
    async def  start_async_wait(self):
        self._task = asyncio.create_task(self._task_async())

    @keyword
    async def wait_for_events(self):
        await self._task
