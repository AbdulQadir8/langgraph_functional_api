import os
from langgraph.func import entrypoint, task
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv, find_dotenv

_: bool = load_dotenv(find_dotenv())

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",
                             google_api_key=os.getenv("GEMINI_API_KEY"))


@task
def poem_genrator(input_data: str) -> str:
    return llm.invoke(f"Genrate a funny poem about {input_data}").content

@task
def poem_evaluator(poem: str) -> str:
    return llm.invoke(f"Evaluate the poem if it is funny or not {poem}.In output only return a score between 0 and 10. Only return int value.").content

@entrypoint()
def evaluator_optimier_workflow(input_data: str):
    while True:
        poem = poem_genrator(input_data).result()
        print("POEM GENRATOR: ", poem)
        evaluation = poem_evaluator(poem).result()
        print("POEM EVALUATION: ", evaluation)
        if int(evaluation) > 5:
            break
        else:
            continue
    return poem

def main():
    poem = evaluator_optimier_workflow.invoke("Vertical AI Agents")
    print("\n\nPOEM: ", poem)

if __name__ == "__main__":
    main()
    