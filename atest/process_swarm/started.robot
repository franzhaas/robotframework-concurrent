*** Settings ***
Library                 robotframework_concurrent.process_star
Test Setup              Test setup keyword
Force Tags              swarm
*** Test Cases ***
basic
    send_message        worki worki
    ${GREET}=           Recv Message
    Log                 ${GREET} from startee

*** Keywords ***
Test setup keyword
    Start_Process
