# Benchmark comparison

| arm | run_id | wall_clock_s | tokens_total | tool_calls | coverage | depth | guardrails | files | bytes | hallucinations | overplan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gsd | bench-todo-gsd-r1 | 180 | 3698 | 4 | 1.00 | 1.00 | 1.00 | 5 | 7602 | 0 | 0 |
| native | bench-todo-native-r1 | 60 | 2108 | 0 | 1.00 | 1.00 | N/A | 1 | 1192 | 0 | 0 |
| no-tools | bench-todo-no-tools-r1 | 90 | 2935 | 0 | 0.93 | 1.00 | 1.00 | 4 | 4485 | 0 | 0 |
| openspec | bench-todo-openspec-r1 | 150 | 3634 | 3 | 1.00 | 1.00 | 1.00 | 5 | 7339 | 0 | 0 |
