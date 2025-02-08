*** Settings ***
Library      async_demo.py
*** Test Cases ***
base demo
    ${R}=     start_async_wait_with_return
    start_async_wait
    start_async_wait
    Log    outside of async
    Sleep      0s
    wait_for_events
    Log    outside of async