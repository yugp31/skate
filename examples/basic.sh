#!/usr/bin/env bash

# Compare two models on a simple prompt
skate run "Explain recursion in one sentence." \
  --models gpt-4o-mini,claude-haiku-4-5-20251001

# Use a prompt file
skate run --prompt-file prompt.txt --models gpt-4o,gemini-1.5-flash

# Template variables
skate run "Translate '{text}' to French." \
  --models gpt-4o-mini \
  --var text="Hello, world"

# With system prompt and temperature
skate run "Write a haiku about autumn." \
  --models gpt-4o,claude-sonnet-4-5 \
  --system "You are a minimalist poet." \
  --temperature 0.9

# Include a local Ollama model
skate run "What is the capital of France?" \
  --models gpt-4o-mini,ollama/llama3
