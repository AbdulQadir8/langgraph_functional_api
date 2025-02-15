from langgraph.func import entrypoint, task


# @task
# def task1():
#     print("Task1")
#     return "Task 1 Completed"

# @task
# def task2():
#     print("Task2")
#     return "Task 2 Completed"


# @entrypoint()
# def run_flow(input: str):
#     print("Running Simple Workflow")

#     task1_output = task1().result()
#     task2_output = task2().result()

#     return f"Workflow executed successfully with outputs: {task1_output} and {task2_output}."

# #Run the workflow
# def run():
#     run_flow.invoke("Simple Input")




#########################################################


@task
def task1():
    print("Task1")
    return "Task 1 Completed"

@task
def task2():
    print("Task2")
    return "Task 2 Completed"


@entrypoint()
def run_flow(input: str):
    task1_output = task1()
    task2_output = task2().result()
    return f"Here is the result of ouputs: {task1_output} and {task2_output}."


def run() -> str:
    for event in run_flow.stream(input="Initiate Task"):
        print(event)