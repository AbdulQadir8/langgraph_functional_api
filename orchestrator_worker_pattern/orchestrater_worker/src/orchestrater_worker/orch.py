from langgraph.func import entrypoint, task
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv, find_dotenv
from pydantic import BaseModel, Field
import os

_: bool = load_dotenv(find_dotenv())

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",
                             google_api_key=os.getenv("GEMINI_API_KEY"))


class InstructionsGenerator(BaseModel):
    worker_instructions: list[str] = Field(description="List of instructions for each worker")

@task
def call_orcherstrator(idea: str) -> InstructionsGenerator:
    instructions = llm.with_structured_output(InstructionsGenerator).invoke(
        f"Generate instructions for the workers to generate a Idea Valiation report for the following idea: {idea}"
    )
    return instructions

@task
def call_worker(instruction: str) -> str:
    return llm.invoke(instruction).content

@task
def combine_results(results: list[str]) -> str:
    return "\n\n".join(results)

@entrypoint()
def orchestrator_worker(idea: str):
    # 0. Call the orchestrator to get the instructions
    instructions = call_orcherstrator(idea).result()
    # 1. Create a list of futures for the workers
    workers = [call_worker(instruction) for instruction in instructions.worker_instructions]
    # 2. Resolve all the futures in parallel
    result = [worker.result() for worker in workers]
    # 3. Combine results
    combined_result = combine_results(result).result()
    return combined_result

def main():
    final_report = orchestrator_worker.invoke("I want to build a startup that makes Solar Electric Vehicles")
    print("\n\n", final_report)


