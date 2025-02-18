# LangGraph Routing Pattern Example

This example demonstrates the implementation of a routing pattern using LangGraph's Functional API. The router randomly assigns incoming messages to different specialized handlers (math, text, or code tasks).

## Features

- Random task routing between math, text, and code handlers
- State management using Pydantic models
- Workflow termination after 3 messages
- Simple message handling demonstration

## Project Structure

```
routing_example/
├── README.md
├── src/
│   └── routing_example/
│       ├── __init__.py
│       └── router.py
```

## Usage

1. Make sure you have the dependencies installed:
```bash
uv add langgraph
```

2. Run the example:
```bash
python -m routing_example.router
```

## How it Works

1. The workflow starts with an initial message
2. The router randomly assigns the message to one of three handlers:
   - Math handler
   - Text handler
   - Code handler
3. Each handler processes the message and adds a response
4. The workflow continues until 3 messages are processed

## Structure

- `src/routing_example/router.py`: Main implementation of the routing pattern
- `State`: Manages the conversation state
- `Message`: Represents individual messages with their task types
- `Graph`: Defines the workflow structure and connections

This is a simplified example to demonstrate the routing pattern concept. In a real application, you would typically implement more sophisticated routing logic based on actual message content or specific requirements.
