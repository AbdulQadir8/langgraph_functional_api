from typing import Dict, List, Optional, Literal
from langgraph.func import entrypoint, task
import random
from pydantic import BaseModel

# Define our message types
class RouterInput(BaseModel):
    query: str

# Define our state
class RouterOutput(BaseModel):
    query: str
    task_type: str
    response: str
@task
def handle_math(message: RouterInput) -> RouterOutput:
    """Handle math-related tasks."""
    return RouterOutput(
        query=message.query,
        task_type= "math",
        response= f"Handled math task for: {message.query}"
    )

@task
def handle_text(message: RouterInput) -> RouterOutput:
    """Handle text-related tasks."""
    return RouterOutput(
        query=message.query,
        task_type= "text",
        response= f"Handled text task for: {message.query}"
    )

@task
def handle_code(message: RouterInput) -> RouterOutput:
    """Handle code-related tasks."""
    return RouterOutput(
        query=message.query,
        task_type= "code",
        response= f"Handled code task for: {message.query}"
    )

@task
def route_message(message: RouterInput) -> Literal["math", "text", "code"]:
    """Route the message to appropriate handler."""
    task_types: Literal["math", "text", "code"] = ["math", "text", "code"]
    return random.choice(task_types)

@entrypoint()
def workflow(input_message: RouterInput) -> RouterOutput:
    """
    Main workflow that processes messages through appropriate handlers.
    
    Args:
        input_message: The input message to process
        
    Returns:
        Dict containing the conversation history
    """    

    # Get the last message
    current_message = input_message.query
    
    # Route the message
    task_type = route_message(RouterInput(query=current_message)).result()
    
    # Handle the message based on the route
    if task_type == "math":
        response = handle_math(RouterInput(query=current_message)).result()
    elif task_type == "text":
        response = handle_text(RouterInput(query=current_message)).result()
    else:  # code
        response = handle_code(RouterInput(query=current_message)).result()
        

    return response

def run_router():
    result = workflow.invoke(RouterInput(query="Hello, this is a test message!"))
    
    print("\nWorkflow Results:")
    print("-" * 50)
    print(f"Content: {result.response}")
    print(f"TaskType: {result.task_type}")
    print("-" * 30) 