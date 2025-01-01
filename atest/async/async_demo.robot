*** Settings ***
Library      async_demo.py
*** Test Cases ***
base demo
    start_async_wait
    start_async_wait
    Log    outside of async
    wait_for_events
    Log    outside of async