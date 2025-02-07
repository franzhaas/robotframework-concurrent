*** Settings ***
Library      concurrent_keyword_demo.py
*** Test Cases ***
base demo
    wait and trigger event
    wait and trigger event
    sleep    2
    poll messages from tasks
    wait for concurrent execution completion


