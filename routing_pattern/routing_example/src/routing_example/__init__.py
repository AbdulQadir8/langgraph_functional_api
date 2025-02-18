"""
Routing example package using LangGraph's Functional API.
"""

from .router import (
    Message,
    State,
    workflow,
    handle_math,
    handle_text,
    handle_code,
    route_message
)

def main() -> None:
    print("Hello from routing-example!")
