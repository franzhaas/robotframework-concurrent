import sys
import subprocess
import multiprocessing.connection
import robot.api.logger as logger
from pathlib import Path
import itertools
from typing import Any, Union
import threading
import queue


class process_star():
    _start_cnt = itertools.count()
    _address = None

    def __init__(self, target_suite: Union[None, Path, str]=None):
        self._target_suite = target_suite        
        self._sp = None

    def Start_Process(self) -> None:
        q = queue.Queue()
        if self._target_suite is None:
            logger.error(process_star._address)
            threading.Thread(target=lambda q: q.put(multiprocessing.connection.Client(process_star._address)), args=(q,)).start()
            try:
                self._fifo = q.get(timeout=2)
            except queue.Empty:
                raise Exception("Child process did not connect to parent process")
            logger.info("started child process")
        else:
            self.out_dir = f"{self._target_suite}_{next(self._start_cnt)}_output"
            fifo = multiprocessing.connection.Listener()
            Path(f"{self.out_dir}").mkdir(parents=True, exist_ok=True)
            self._stdout = open(f"{self.out_dir}/output.log", "w")
            self._sp = subprocess.Popen([sys.executable, "-c", fr"""
import robotframework_concurrent.process_star
import robot
robotframework_concurrent.process_star.process_star._address = r"{fifo.address}"
robot.run("{self._target_suite}", outputdir='{self.out_dir}')
"""], stdout=self._stdout, stderr=subprocess.STDOUT)
            threading.Thread(target=lambda q: q.put(fifo.accept()), args=(q,)).start()
            try:
                self._fifo = q.get(timeout=10)
            except queue.Empty:
                raise Exception("Child process did not connect to parent process")
            logger.info(f"Initiated start of process for suite: {self._target_suite} with output dir: {self.out_dir}")

    def send_message(self, message: Any) -> None:
        self._fifo.send(message)

    def recv_message(self) -> Any:
        return self._fifo.recv()
    
    def Process_Should_Have_Terminated(self, timeout:int =1) -> None:
        assert self._sp is not None, "Process was not started"
        try:
            self._sp.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            raise Exception(f"Process {self._target_suite} has not terminated(output: {self._out_dir})")
        
    def Process_Should_Be_Running(self) -> None:
        assert self._sp is not None, "Process was not started"
        try:
            self._sp.wait(timeout=0)
            raise Exception(f"Process {self._target_suite} has terminated prematurely (output: {self._out_dir})")
        except subprocess.TimeoutExpired:
            pass
    
    def __del__(self):
        if self._sp is not None:
            try:
                self._sp.wait(timeout=1)
            except subprocess.TimeoutExpired:
                logger.error(f"Process star was not terminated properly (suite: {self._target_suite}, output: {self._out_dir}), killing it.")
                self._sp.kill()
                self._sp.wait(timeout=2)
