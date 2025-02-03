*** Settings ***
Library           tcp_example.py
*** Tasks ***
select based parallelism
    ${ROBOTFRAMEWORK}=       connect_http_bare   www.robotframework.org    80
    ${ROBOCON}=              connect_http_bare   www.robocon.io    80
    Send Request Bare        ${ROBOTFRAMEWORK}   GET / HTTP/1.1\r\n\r\n
    Send Request Bare        ${ROBOCON}          GET / HTTP/1.1\r\n\r\n
    @{READABLES}=            get_readables   ${ROBOTFRAMEWORK}   ${ROBOCON}
    WHILE    @{READABLES}
        consume data from sockets   @{READABLES}
        @{READABLES}=            get_readables   ${ROBOTFRAMEWORK}   ${ROBOCON}
    END

*** Keywords ***
consume data from sockets
    [Arguments]   @{READABLES}
    FOR  ${SOCKET}    IN     @{READABLES}
        ${DATA}=     get_data   ${SOCKET}
    END
