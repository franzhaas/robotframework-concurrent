import time
import robot.api.logger as logger
from pathlib import Path
import itertools
from typing import Any, Union
from robot.libraries.BuiltIn import BuiltIn
import pathlib

try:
    import interpreters
except ImportError:
    from interpreters_backport import interpreters


class interpreter_star():
    _start_cnt = itertools.count()
    _address = None


    def __init__(self, target_suite: Union[None, Path, str]=None):
        self._target_suite = target_suite        
        self._interpreter = None


    def Start_interpreter(self) -> None:
        if self._target_suite:
            logger.trace(f"starting: {self._target_suite} in a subinterpreter")
            builtInInst = BuiltIn()
            odir = pathlib.Path(builtInInst.get_variable_value("${OUTPUT_DIR}"))
            loglevel = builtInInst.get_variable_value("${LOG LEVEL}")
            self.out_dir = str(odir / f"{self._target_suite}_{next(self._start_cnt)}_output")
            self._inQ = interpreters.create_queue()
            self._outQ = interpreters.create_queue()
            self._interpreter = interpreters.create()

            def _start_robotframework_in_subinterpreter():
                import __main__
                import robot
                import robotframework_concurrent.interpreter_star
                import pathlib
                try:
                    import interpreters
                except ImportError:
                    from interpreters_backport import interpreters
                
                outdir = pathlib.Path(getattr(__main__, "__out_dir"))
                outdir.mkdir(parents=True, exist_ok=True)

                with open(outdir / "output.log", "w", buffering=1) as stdout:
                    robotframework_concurrent.interpreter_star.interpreter_star._inQ = interpreters.Queue(getattr(__main__, "__outQ"))
                    robotframework_concurrent.interpreter_star.interpreter_star._outQ = interpreters.Queue(getattr(__main__, "__inQ"))
                    robotframework_concurrent.interpreter_star.interpreter_star._outQ.put("started")
                    robot.run(getattr(__main__, "__target_suite"), outputdir=getattr(__main__, "__out_dir"), stdout=stdout, stderr=stdout, loglevel=getattr(__main__, "__loglevel"))

            self._interpreter.prepare_main(__outQ=self._outQ.id, __inQ=self._inQ.id, __out_dir=self.out_dir, __target_suite=self._target_suite, __loglevel=loglevel)
            self._subinterpreter_thread = self._interpreter.call_in_thread(_start_robotframework_in_subinterpreter)
            try:
                assert "started" == self._inQ.get(timeout=10), "Subinterpreter did not start"
            except interpreters.QueueEmpty:
                raise Exception("Subinterpreter did not start")
            logger.info(f"started: {self._target_suite} in a subinterpreter, output is available at.: {self.out_dir}")


    def send_message(self, message: Any) -> None:
        if self._interpreter:
            assert self._interpreter.is_running(), "Interpreter has terminated"
        self._outQ.put(message)


    def recv_message(self, timeout:int=None) -> Any:
        if self._interpreter and self._interpreter.is_running() is False:
            try:
                return self._inQ.get_nowait()
            except interpreters.QueueEmpty:
                raise Exception(f"Interpreter {self._target_suite} has terminated and did not leave any messages")
        return self._inQ.get(timeout=timeout)


    def interpreter_Should_Have_Terminated(self, timeout:int=1) -> None:
        assert self._interpreter is not None, "Process was not started"
        deadline = time.time() + timeout
        while self._interpreter.is_running() and time.time() < deadline:
            time.sleep(0.1)
        assert not self._interpreter.is_running(), f"Process {self._target_suite} has not terminated within {timeout} seconds"


    def interpreter_Should_Be_Running(self) -> None:
        assert self._sp is not None, "Process was not started"
        if not self._interpreter.is_running():
            raise Exception(f"Process {self._target_suite} has terminated prematurely (output: {self._out_dir})")
