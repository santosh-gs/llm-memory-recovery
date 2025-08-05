# Simultaneous Query Output and Memory

### Query 1
When a complex prompt is passed, related memories are separated and are stored as separated entries:  

![Query 1](https://github.com/santosh-gs/llm-memory-recovery/blob/main/images/query_1_output_and_memory.png?raw=true)

### Query 2
Simultaneous addition and deletion of memory entries: 

![Query 2](https://github.com/santosh-gs/llm-memory-recovery/blob/main/images/query_2_output_and_memory.png?raw=true)

### Queries 3 and 4

![Queries 3 and 4](https://github.com/santosh-gs/llm-memory-recovery/blob/main/images/query_3_and_4_output_and_memory.png?raw=true)

### Queries 5 and 6
When deleting a part of a single memory entry, the previous (existing) memory entry gets deleted and a new memory entry is created with only the relevant information.

![Queries 5 and 6](https://github.com/santosh-gs/llm-memory-recovery/blob/main/images/query_5_and_6_output_and_memory.png?raw=true)

### Query 7
Retrieval of updated information:

![Query 7](https://github.com/santosh-gs/llm-memory-recovery/blob/main/images/query_7_output_and_memory.png?raw=true)

### Additional Memory Managaement Queries
One can use the following queries to directly manage the memory:
* List all the memory entries
* Delete all memory
* List all the memory related to sports and food
* Delete memory associated with games
