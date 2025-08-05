# System Design

![System Design Visualization](https://github.com/santosh-gs/llm-memory-recovery/blob/main/images/system_design.png?raw=true)

## High Level Architecture

| Component                                    | Purpose |
|----------------------------------------------|---------|
| **LangChain**                                | Framework for chaining LLM calls, retrieval, memory, and prompt templates |
| **Chroma**                                 | Vector database for storing and retrieving embedded memory and document chunks |
| **SQLite Database**                             | Persistent storage for memory metadata, IDs, and user-specific memory lists |
| **CSV / JSON** | An indexed SQLite database offers efficient lookups (O(log n)) compared to CSV / JSON (O(n) because it involves reading and writing). CSV in this setup is primarily used for human-readable logging and tracking of memory updates |
| **OpenAI Embedding Model (text-embedding-ada-002)** | Converts text into vector embeddings for similarity search |
| **OpenAI Chat Model (gpt-4.1, -mini, -nano, etc.)** | Generates responses, processes queries, and returns structured memory actions |
| **RecursiveCharacterTextSplitter**           | Splits documents (memory here) into smaller overlapping chunks for better retrieval accuracy (500 + 250 overlap used here) |
| **Retriever (.as_retriever)**                | Fetches the most relevant memory chunks from the vector store for prompt injection |
| **Similarity Search Algorithm (Cosine/Euclidean)** | Finds the closest matching stored memory vectors to a given query. The default for Chroma is Euclidean Distance algorithm |
| **UUID / ID Generator**                      | Assigns unique IDs to stored memory entries for easy deletion and updates |
| **Memory Deletion & Update Mechanism**       | Handles user or LLM-triggered removal or modification of stored memories |
| **Persistence Layer**                        | Saves vector store and metadata to disk so memory survives application restarts. Automatically handled by Chroma |


### System Prompt (Few-Shot Technique)
* The system prompt enforces a strict response format where the LLM outputs both a natural language reply and a structured memory action, separated by a special delimiter.
* It uses **few-shot prompting** with multiple examples to teach the model how to handle various memory operations like ***add*** **(by Memory Context)**, ***delete*** **(by Memory ID)**, or ***ignore***.
* The LLM extracts the key fact from the user message and appends it with the ***add*** action. For deletions, it appends the corresponding Memory ID with the ***delete*** action.
* Deleting by Memory ID ensures accurate targeting of the memory entry while reducing token usage compared to deleting by memory text. 
* **Few-shot** prompting is preferred over **one-shot** in this case, as the action format is rigid and requires consistent response structure. Few-shot examples guide the LLM to produce correctly formatted responses across various types of responses.


