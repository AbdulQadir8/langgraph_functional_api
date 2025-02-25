import os
from langgraph.func import entrypoint, task
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv, find_dotenv
from langgraph.prebuilt import create_react_agent
load_dotenv(find_dotenv())

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",google_api_key=os.getenv("GEMINI_API_KEY"))

agent = create_react_agent(
        model=llm,
        tools=[],
        prompt="""
        You are a helpful assistant that can answer questions and help with tasks.
        """
    )


def main():
    result = agent.invoke({"messages": "What is the capital of the moon?"})
    print("\n\nResult",result)


if __name__ == "__main__":
    main()

