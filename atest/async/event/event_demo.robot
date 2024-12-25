*** Settings ***
Library      eventDemo.py
*** Test Cases ***
base demo
    wait_and_trigger_event
    wait_and_trigger_event
    wait_for_async_execution_completion