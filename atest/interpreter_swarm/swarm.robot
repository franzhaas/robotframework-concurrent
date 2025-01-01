*** Settings ***
Library                 robotframework_concurrent.interpreter_star   atest/interpreter_swarm/started.robot       WITH NAME      interpreter1
Library                 robotframework_concurrent.interpreter_star   atest/interpreter_swarm/started2.robot      WITH NAME      interpreter2
Test Setup              Test setup keyword
Test Teardown           Test teardown keyword
*** Test Cases ***
basic
    interpreter1.Send Message        order order
    interpreter2.Send Message        reorder reorder
    ${GREET}=           interpreter1.Recv Message
    Log                 ${GREET} from star
    ${GREET}=           interpreter2.Recv Message
    Log                 ${GREET} from star2

basic2
    interpreter1.Send Message        order order
    interpreter2.Send Message        reorder reorder
    ${GREET}=           interpreter1.Recv Message
    Log                 ${GREET} from star1
    ${GREET}=           interpreter2.Recv Message
    Log                 ${GREET} from star2
*** Keywords ***
Test setup keyword
    interpreter1.Start_interpreter
    interpreter2.Start_interpreter

Test teardown keyword
    interpreter1.interpreter_Should_Have_Terminated
    interpreter2.interpreter_Should_Have_Terminated
