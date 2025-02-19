"""
Assistant Selector using LangGraph's Functional API.

This package demonstrates how to build an intelligent assistant selector
that routes queries to specialized assistants based on their expertise and confidence.
"""

from .workflow import (
    InputState,
    OutputState,
    code_assistant,
    complex_assistant,
    simple_assistant,
    select_assistant,
    run_example
)

def main() -> None:
    print("Hello from assistant-selector!")
