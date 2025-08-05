# System Design

![System Design Visualization](https://github.com/santosh-gs/llm-memory-recovery/blob/main/images/system_design.png?raw=true)

## Salient Features

### System Prompt (Few-Shot Technique)
* The system prompt enforces a strict response format where the LLM outputs both a natural language reply and a structured memory action, separated by a special delimiter.
* It uses **few-shot prompting** with multiple examples to teach the model how to handle various memory operations like ***add*** **(by Memory Context)**, ***delete*** **(by Memory ID)**, or ***ignore***.
* The LLM extracts the key fact from the user message and appends it with the ***add*** action. For deletions, it appends the corresponding Memory ID with the ***delete*** action.
* Deleting by Memory ID ensures accurate targeting of the memory entry while reducing token usage compared to deleting by memory text. 
* **Few-shot** prompting is preferred over **one-shot** in this case, as the action format is rigid and requires consistent response structure. Few-shot examples guide the LLM to produce correctly formatted responses across diverse cases.
