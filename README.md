# LLM Memory Recovery

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


### LLM Instructions
* You will asked to prompt your query as follows  
`Ask your question (q to quit):` give your prompt  
* If the model thinks any info within the prompt is worth remembering. Check `system_prompt.txt` for detailed analysis that takes place.
* Prompt `q` to quit.

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
* Check `system_prompt.txt` for detailed instructions and examples.