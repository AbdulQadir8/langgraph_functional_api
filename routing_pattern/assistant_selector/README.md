# Assistant Selector

A smart assistant routing system built with LangGraph's Functional API that demonstrates how to route queries to specialized assistants based on their expertise and confidence levels.

## Features

- Multiple specialized assistants (Code, Math, Writing)
- Confidence-based routing
- Context-aware query handling
- Parallel assistant evaluation
- Clean functional implementation using LangGraph

## Project Structure

```
assistant_selector/
├── README.md
├── src/
│   └── assistant_selector/
│       ├── __init__.py
│       └── selector.py
```

## Usage

1. Install dependencies:
```bash
uv add langgraph
```

2. Run the example:
```bash
python -m assistant_selector.selector
```

## How it Works

1. The workflow receives a query with optional context
2. All specialized assistants evaluate the query in parallel:
   - Code Assistant: Specialized in programming tasks
   - Math Assistant: Handles mathematical calculations
   - Writing Assistant: Focuses on text composition
3. Each assistant provides a confidence score
4. The selector chooses the most confident assistant
5. The selected assistant's response is returned

## Example

```python
from assistant_selector import workflow, Query

# Create a query
query = Query(text="Help me write a Python function")

# Get response from most appropriate assistant
result = workflow.invoke(query)
print(f"Selected: {result.assistant_type}")
print(f"Response: {result.response}")
```

## Implementation Details

- Uses LangGraph's Functional API with `@task` and `@entrypoint` decorators
- Pydantic models for type safety and validation
- Confidence-based selection mechanism
- Parallel task execution for better performance

This is a demonstration project showing how to implement intelligent query routing using LangGraph. In a production environment, you would typically:
1. Implement more sophisticated confidence scoring
2. Add more specialized assistants
3. Include error handling and fallback mechanisms
4. Add logging and monitoring
