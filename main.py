# System Imports
import os
import uuid
import csv
from typing import List
from dotenv import load_dotenv

# Langchain Imports
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# LLM Specific Imports
from openai import OpenAI


# Load API Key
load_dotenv()
print("Environment loaded successfully")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Constants
USER_ID = "user0"
MODEL_NAME = "gpt-4o"
TEMPERATURE = 0.7
DATA_DIR = "./data"
PROMPT_FILE = "./system_prompt.txt"
CHROMA_DIR = os.path.join(DATA_DIR, f"chroma_{USER_ID}")
MEMORY_FILE = os.path.join(DATA_DIR, f"persistent_memory_{USER_ID}.csv")

os.makedirs(DATA_DIR, exist_ok=True)

# Initialize
print("Initializing models...")
llm = ChatOpenAI(model=MODEL_NAME, temperature=TEMPERATURE)
embedding_model = OpenAIEmbeddings()
vectorstore = Chroma(
    persist_directory=CHROMA_DIR,
    embedding_function=embedding_model,
    collection_name="memory"
)
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=250)
print("Models initialized successfully")


# CSV Handlers
def load_memories_csv() -> List[dict]:
    if not os.path.exists(MEMORY_FILE):
        return []
    with open(MEMORY_FILE, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def save_memory_csv(memory_id: str, memory_text: str):
    file_exists = os.path.isfile(MEMORY_FILE)
    with open(MEMORY_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'memory'])
        if not file_exists:
            writer.writeheader()
        writer.writerow({'id': memory_id, 'memory': memory_text})
    print(f"Added to Memory: {memory_text}")


def delete_memory_csv(memory_id: str):
    rows = load_memories_csv()
    deleted_memory = ""
    with open(MEMORY_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'memory'])
        writer.writeheader()
        for row in rows:
            if row['id'] != memory_id:
                writer.writerow(row)
            else:
                deleted_memory = row['memory']
    if deleted_memory:
        print(f"Deleted from Memory: {deleted_memory}")


# Chroma Memory Operations
def add_memory(memory_text: str):
    doc_id = str(uuid.uuid4())
    doc = Document(
        page_content=memory_text,
        metadata={"id": doc_id, "status": "active"}
    )
    split_docs = splitter.split_documents([doc])
    vectorstore.add_documents(split_docs)
    save_memory_csv(doc_id, memory_text)
    # vectorstore.persist()  # Automatically gets persisted
    return doc_id


def delete_memory_by_id(memory_id: str):
    vectorstore.delete(ids=[memory_id])
    # vectorstore.persist() # Automatically gets persisted
    delete_memory_csv(memory_id)


def handle_memory_actions(actions: List[str]):
    for action in actions:
        if action.startswith("addÿ"):
            mem = action.replace("addÿ", "").strip()
            if mem:
                add_memory(mem)
        elif action.startswith("deleteÿ"):
            mem_id = action.replace("deleteÿ", "").strip()
            if mem_id:
                delete_memory_by_id(mem_id)


# Answer Query with Memory Awareness
def answer_query(query: str) -> str:
    retriever = vectorstore.as_retriever()
    try:
        docs = retriever.invoke(query)
    except Exception as e:
        return f"Retriever error: {e}"

    # if not docs:
    #     return "I couldn't find any memory related to that."

    context = "\n".join([doc.page_content for doc in docs])

    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        system_prompt = f.read()

    prompt = f"""
Based on the following memory entries, answer the question:
MEMORIES:
{context}

QUESTION:
{query}
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt.strip()}
        ],
        temperature=TEMPERATURE
    )

    full = response.choices[0].message.content.strip()
    print(f"full: {full}")
    parts = full.split("þ")
    print(f"parts: {parts}")
    main_response = parts[0].strip()
    print(f"main_response: {main_response}")
    memory_actions = parts[1:] if len(parts) > 1 else []
    print(f"memory_actions: {memory_actions}")

    handle_memory_actions(memory_actions)
    return main_response


# Chat Loop
def chat_loop():
    print("Starting LLM...\n\n")
    while True:
        print("\n\n-------------------------------")
        question = input("Ask your question (q to quit): ")
        print("\n\n")
        if question.lower() == "q":
            break
        response = answer_query(question)
        print(response)


if __name__ == "__main__":
    print("Loaded docs")
    chat_loop()
