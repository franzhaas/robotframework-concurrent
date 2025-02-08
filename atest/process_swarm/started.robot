*** Settings ***
Library                 robotframework_concurrent.process_star
Test Setup              Test setup keyword
Force Tags              swarm
*** Test Cases ***
basic
    ${msg}=           Recv Message
    ${msg}=           Evaluate  ${msg} + 1
    send_message      ${msg}
    Log               ${msg} from startee

*** Keywords ***
Test setup keyword
    Start_Process
