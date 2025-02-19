from typing import  Literal, cast
from pydantic import BaseModel
import random
from dotenv import load_dotenv, find_dotenv
from langgraph.func import entrypoint, task
from langchain_google_genai import ChatGoogleGenerativeAI
import os

_: bool = load_dotenv(find_dotenv())

# Initialize different model instances
router_model = ChatGoogleGenerativeAI(model="gemini-1.5-flash-8b-001",api_key=os.getenv("GEMINI_API_KEY"))
simple_model = ChatGoogleGenerativeAI(model="gemini-1.5-flash",api_key=os.getenv("GEMINI_API_KEY"))
advanced_model = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp",api_key=os.getenv("GEMINI_API_KEY"))
reasoning_coding_model = ChatGoogleGenerativeAI(model="gemini-2.0-flash-thinking-exp-01-21",api_key=os.getenv("GEMINI_API_KEY"))

class InputState(BaseModel):
    """Input query model."""
    query: str

class OutputState(BaseModel):
    """Response model from assistants."""
    query: str
    assistant_type: str
    response: str

QuestionType = Literal["simple", "complex", "code"]

class QuestionClassifier(BaseModel):
    type: QuestionType

@task
def code_assistant(query: InputState) -> str:
    """Handle code-related questions using the advanced model with specific instructions."""
    prompt = f"""Please provide a detailed answer with code examples where appropriate.
    Include explanations of the code and best practices.

    Question: {query.query}"""
    response = reasoning_coding_model.invoke(prompt)
    return response.content
@task
def simple_assistant(query: InputState) -> str:
    """Handle simple questions using the basic model."""
    prompt = f"""Please provide a clear and concise answer to this question: {
        query.query}"""

    response = simple_model.invoke(prompt)
    return response.content

@task
def complex_assistant(query: InputState) -> str:
    """Handle complex questions using the advanced model."""
    prompt = f"""Please provide a detailed, well-reasoned answer to this question: {
        query.query}"""
    response = advanced_model.invoke(prompt)
    return response.content
@task
def select_assistant(query: InputState) -> QuestionClassifier:
    """Classify the question to determine which model should handle it."""
    prompt = """Analyze the following question and classify it as either:
    - 'simple': For basic, factual, or common questions
    - 'complex': For questions requiring deep analysis, reasoning, or expertise
    - 'code': For questions about programming or technical implementations
    
    Respond with ONLY the classification word.
    
    Question: {question}
    """


    response = cast(QuestionClassifier, router_model.with_structured_output(QuestionClassifier).invoke(prompt.format(question=query.query)))
    result = response.type
    print(f"Type: {result}")
    if result not in ['simple',"complex","code"]:
        return "complex" # return complex if classifica
    else:
        return result     

@entrypoint()
def workflow(query: InputState) -> OutputState:
    """
    Main workflow that selects and routes to the most appropriate assistant.
    
    Args:
        query: The input query with optional context
        
    Returns:
        Response from the most appropriate assistant
    """
 

    
    # Select the most appropriate assistant
    selected = select_assistant(query=query).result()

    # Return the response from the selected assistant
    if selected == "code":
        response = code_assistant(query).result()
        return OutputState(query=query.query,
                           response=response,
                           assistant_type=selected)
    elif selected == "simple":
        response = simple_assistant(query).result()
        return OutputState(query=query.query,
                           response=response,
                           assistant_type=selected)
    else:
        response = complex_assistant(query).result()
        return OutputState(query=query.query,
                           response=response,
                           assistant_type=selected)

def run_example():
    # Example queries
    queries = [
        "Help me write a Python function",
        "Calculate the square root of 16",
        "Write an essay about AI"
    ]
    query_text = random.choice(queries)
    
    print("\nAssistant Selector Demo")
    print("-" * 50)
    
    result = workflow.invoke(input=InputState(query=query_text))
    print(f"\nQuery: {result.query}")
    print(f"Selected Assistant: {result.assistant_type}")
    print(f"Response: {result.response}")
    print("-" * 30)

 