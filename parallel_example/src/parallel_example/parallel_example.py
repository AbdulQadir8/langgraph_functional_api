from typing import List
import os
import time
from langgraph.func import task, entrypoint
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()

# Initialize Gemini model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",api_key=os.getenv("GEMINI_API_KEY"))

@task
def process_task(task: str) -> str:
    """Process a single task using Gemini."""
    try:
        time.sleep(3)
        response = llm.invoke(f"Complete this task: {task}")
        return response.content
    except Exception as e:
        return f"Error: {str(e)}"

@entrypoint()
def parallel_tasks(tasks: List[str]) -> List[str]:
    """Process multiple tasks in parallel."""
    # Submit all tasks for parallel processing
    futures = [process_task(task) for task in tasks]
    
    # Return results as they complete
    return [future.result() for future in futures]

def parallel_flow():
    # Example tasks
    tasks = [
        "Write a haiku about coding",
        "List 3 Python tips",
        "Define parallel processing"
    ]
    
    # Run tasks and print results
    print("Processing tasks...\n")
    start_time = time.time()
    results = parallel_tasks.invoke(tasks)
    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")
    # Print results
    for task, result in zip(tasks, results):
        print(f"Task: {task}")
        print(f"Result: {result}\n")

