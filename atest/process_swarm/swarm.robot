*** Settings ***
Library                 robotframework_concurrent.process_star   atest/process_swarm/started.robot       WITH NAME      process1
Library                 robotframework_concurrent.process_star   atest/process_swarm/started2.robot       WITH NAME      process2
Test Setup              Test setup keyword
Test Teardown           Test teardown keyword
*** Test Cases ***
basic1
    process1.Send Message        ${1}
    process2.Send Message        ${2}
    ${msg}=                      process1.Recv Message
    Should Be Equal As Integers  ${msg}  ${2}
    ${msg}=                      process2.Recv Message
    Should Be Equal As Integers  ${msg}  ${4}

basic2
    process1.Send Message        ${1}
    process2.Send Message        ${2}
    ${msg}=                      process2.Recv Message
    Should Be Equal As Integers  ${msg}  ${4}
    ${msg}=                      process1.Recv Message
    Should Be Equal As Integers  ${msg}  ${2}


*** Keywords ***
Test setup keyword
    process1.Start_Process
    process2.Start_Process

Test teardown keyword
    process1.Process_Should_Have_Terminated
    process2.Process_Should_Have_Terminated