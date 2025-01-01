*** Settings ***
Library                  robotframework_concurrent.interpreter_star
Test Setup              Test setup keyword
Force Tags              swarm
*** Test Cases ***
basic
    send_message        sleepi sleepi
    ${GREET}=           Recv Message
    Log                 ${GREET} from startee

*** Keywords ***
Test setup keyword
    Start_interpreter
