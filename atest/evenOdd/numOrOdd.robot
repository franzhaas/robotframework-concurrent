*** Settings ***
Library           evenOrOdd.py
*** Test Cases ***
basic
    odd       8000000
    odd       8000001
    wait_for_concurrent_execution_completion