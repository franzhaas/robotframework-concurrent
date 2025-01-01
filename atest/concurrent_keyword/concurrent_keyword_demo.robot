*** Settings ***
Library      concurrent_keyword_demo.py
*** Test Cases ***
base demo
    wait_and_trigger_event
    wait_and_trigger_event
    sleep    2
    poll_messages_from_tasks
    wait_for_concurrent_execution_completion