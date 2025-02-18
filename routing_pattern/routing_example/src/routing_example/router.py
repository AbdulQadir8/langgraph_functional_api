from typing import Dict, List, Optional
from langgraph.func import entrypoint, task
import random
from pydantic import BaseModel

# Define our message types
class Message(BaseModel):
    content: str
    task_type: Optional[str] = None

# Define our state
class State(BaseModel):
    messages: List[Message]
    current_task: Optional[str] = None

@task
def handle_math(message: Message) -> Message:
    """Handle math-related tasks."""
    return Message(
        content=f"Handled math task for: {message.content}",
        task_type="math"
    )

@task
def handle_text(message: Message) -> Message:
    """Handle text-related tasks."""
    return Message(
        content=f"Handled text task for: {message.content}",
        task_type="text"
    )

@task
def handle_code(message: Message) -> Message:
    """Handle code-related tasks."""
    return Message(
        content=f"Handled code task for: {message.content}",
        task_type="code"
    )

@task
def route_message(message: Message) -> str:
    """Route the message to appropriate handler."""
    task_types = ["math", "text", "code"]
    return random.choice(task_types)

@entrypoint()
def workflow(input_message: str) -> Dict:
    """
    Main workflow that processes messages through appropriate handlers.
    
    Args:
        input_message: The input message to process
        
    Returns:
        Dict containing the conversation history
    """
    # Initialize state
    state = State(messages=[Message(content=input_message)])
    
    # Process up to 3 messages
    for _ in range(3):
        # Get the last message
        current_message = state.messages[-1]
        
        # Route the message
        task_type = route_message(current_message).result()
        
        # Handle the message based on the route
        if task_type == "math":
            response = handle_math(current_message).result()
        elif task_type == "text":
            response = handle_text(current_message).result()
        else:  # code
            response = handle_code(current_message).result()
            
        # Update state
        state.messages.append(response)
    
    return {
        "messages": [msg.dict() for msg in state.messages],
        "final_task_type": state.messages[-1].task_type
    }

def run_router():
    result = workflow.invoke("Hello, this is a test message!")
    
    print("\nWorkflow Results:")
    print("-" * 50)
    for i, msg in enumerate(result["messages"], 1):
        print(f"Message {i}:")
        print(f"Content: {msg['content']}")
        print(f"Task Type: {msg['task_type']}")
        print("-" * 30) 