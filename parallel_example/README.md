# Simple LangGraph Parallel Tasks Example

A minimal example demonstrating parallel task processing using LangGraph's Functional API with Google's Gemini model.

## Features

- Simple parallel task processing with `@task` decorator
- Integration with Google's Gemini model
- Clean and straightforward implementation

## Setup

1. Create a `.env` file with your Google API key:
```
GOOGLE_API_KEY=your_api_key_here
```

2. Install dependencies using UV:
```bash
uv add langgraph langchain-google-genai python-dotenv
```

## Running the Example

```bash
python parallel_example.py
```

## How it Works

1. `@task` decorator enables parallel execution
2. `@entrypoint` defines the main workflow
3. Tasks are processed concurrently using Gemini
4. Results are collected and displayed

## Customization

Modify the tasks list in `main()` to process different queries with Gemini.
