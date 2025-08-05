# Long term memory for LLMs (LLM Memory Recovery)

![System Design Visualization](https://github.com/santosh-gs/llm-memory-recovery/blob/main/images/system_design.png?raw=true)

Check [`test_ouput.md`](https://github.com/santosh-gs/llm-memory-recovery/blob/main/test_output.md) for tested prompts and simulataneous memory updates that happen.

## Instructions
### Download the repository
* Go to a terminal and paste `git clone https://github.com/santosh-gs/llm-memory-recovery.git`

### OpenAI API Key
Before you begin, set up an OpenAI account and generate a new key. You will need to put your credentials in a `.env` file.
* Go to https://platform.openai.com/api-keys and create an OpenAI key.
* Create a `.env` file in your project directory and add `OPENAI_API_KEY="your_generated_secret_key"`.
* The `.gitignore` file will ensure that your API key remain in your local system.

### Running the application
Inside a terminal, run the following:
* Navigate to the cloned folder using `cd /llm-memory-recovery`
* Create a virtual environment using `python -m venv myenv` (Optional if you already have the required libraries)
* Activate the virtual enviroment (if any) using  
`myenv\Scripts\activate` (if using Windows Command Prompt)  
`.\myenv\Scripts\Activate.ps1` (if using Windows PowerShell)  
`source myenv/Scripts/activate` (if using git bash or bash in Mac or Linux system)  

* Install dependencies `pip install -r requirements.txt`
* Run `python main.py` in the terminal or open the folder in a code editor like VS Code

Note: Do not open the `persistent_memory_user.csv` in excel while running the llm as it locks the file to read-only mode and prevents modifications.  
Rather open it in VS Code to track live memory updates.


### LLM Instructions
* You will asked to prompt your query as follows  
`Ask your question (q to quit):` give your prompt  
* If the model thinks any info within the prompt is worth remembering. Check `system_prompt.txt` for detailed analysis that takes place.
* Prompt `q` to quit.

### Example Prompts
* Hi, I am Santosh. I like PyTorch and TensorFlow. In which years were these frameworks released?
* I like apples, bananas, and chess. Which of apple and banana contain more protein per fruit?
* Who am I?
* What do you know about me? List everything
* Which frameworks do I like?
* I no longer like TensorFlow, it's so overwhelming.
* Which frameworks do I like now?

The memory is stored in `persistent_memory_user0.csv` in the `data` folder. As long as the user remains same, the memory persists and can be recalled.  

If you want to start over, prompt `delete all memory` or change `USER_ID` variable to something like `user1`.

## Prompt Engineering
* Here, I have used rarely used ASCII characters `þ` and `ÿ` as separators between response and action to be taken regarding memory.
* The actions include `add` `delete` `ignore` 

### `ignore` action
* Just respond to query and need not add any info to memory.

### `add` action
* Add concise summarized key statements to memory.

### `delete` action
* Delete memory entry that's no longer needed.

### Updating Existing Memory Entry
* To update an existing memory entry, we use `add` and `delete` one after the other  
`add` final desired entry  
`delete` existing entry  
e.g. suppose a memory entry can be "User like Cricket and Football" 
Now if the user no longer likes Football, we run:  
`add` "User likes Cricket"
`delete` "User like Cricket and Football"
* Check [`system_prompt.txt`](https://github.com/santosh-gs/llm-memory-recovery/blob/main/system_prompt.txt) for detailed instructions and examples.