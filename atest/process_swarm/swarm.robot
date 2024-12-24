*** Settings ***
Library                 robotframework_concurrent.process_swarm   started.robot       WITH NAME      process1
Library                 robotframework_concurrent.process_swarm   started2.robot       WITH NAME      process2
Test Setup              Test setup keyword
Test Teardown           Test teardown keyword
*** Test Cases ***
basic   
    process1.Send Message        order order
    process2.Send Message        reorder reorder
    ${GREET}=           process1.Recv Message
    Log                 ${GREET} from swarm
    ${GREET}=           process2.Recv Message
    Log                 ${GREET} from swarm2

basic2
    process1.Send Message        order order
    process2.Send Message        reorder reorder
    ${GREET}=           process1.Recv Message
    Log                 ${GREET} from swarm1
    ${GREET}=           process2.Recv Message
    Log                 ${GREET} from swarm2
*** Keywords ***
Test setup keyword
    process1.Start_Process
    process2.Start_Process

Test teardown keyword
    process1.Process_Should_Have_Terminated
    process2.Process_Should_Have_Terminated