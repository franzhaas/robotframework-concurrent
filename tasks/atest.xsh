uv sync --extra test --extra interpreters

uv run robot  -L TRACE -e swarm -e interpreter_swarm -P atest/interpreter_swarm/ -P atest/process_swarm/ -P atest/evenOdd/ atest
