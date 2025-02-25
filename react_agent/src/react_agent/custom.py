from langgraph.func import entrypoint, task
from langgraph.graph.message import add_messages

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool

from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",
                             google_api_key=os.getenv("GEMINI_API_KEY"))

promt = "You are a helpful assistant that can answer questions and help with tasks."

@tool
def get_weather(location: str) -> str:
    """Get the weather in a given location"""
    # This is the placeholer for the actual implementation
    if any([city in location.lower() for city in ["lahore", "lhr"]]):
        return "The weather in Lahore is sunny"
    elif "karachi" in location.lower():
        return "The weather in Karachi is cloudy"
    else:
        return f"Sorry, I don't know the weather in {location}"

tools = [get_weather]

tools_by_name = {tool.name: tool for tool in tools}

@task
def call_model(messages):
    """call model with a sequence of messages"""
    response = llm.bind_tools(tools).invoke(messages)
    return response

@task
def call_tool(tool_call):
    tool = tools_by_name[tool_call["name"]]
    observation = tool.invoke(tool_call["args"])
    return ToolMessage(content=observation, tool_call_id=tool_call["id"], name=tool_call["name"])


@entrypoint()
def agent(messages):
    llm_response = call_model(messages).result()
    while True:
        if not llm_response.tool_calls:
            break
        #Execute tools
        tool_result_futures = [call_tool(tool_call) for tool_call in llm_response.tool_calls]
        tool_results = [fut.result() for fut in tool_result_futures]
        
        # Append to message list
        messages = add_messages(messages, [llm_response, *tool_results])

        #call model again
        llm_response = call_model(messages).result()

    return llm_response

def main():
    user_message = {"role": "user", "content": "Use get weather tool and share what's the weather in karachi"}
    
    for step in agent.stream([user_message]):
        for message in step.values():
            message.pretty_print()
