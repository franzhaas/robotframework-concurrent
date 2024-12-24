*** Settings ***
Library                  robotframework_concurrent.process_swarm
Test Setup              Test setup keyword
*** Test Cases ***
basic
    send_message        sleepi sleepi
    ${GREET}=           Recv Message
    Log                 ${GREET} from startee

*** Keywords ***
Test setup keyword
    Start_Process
