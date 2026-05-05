#!/usr/bin/env bash

# Pick a winner using gpt-4o as judge
skate run "Explain the difference between TCP and UDP." \
  --models gpt-4o-mini,claude-haiku-4-5-20251001 \
  --judge gpt-4o

# Judge with explicit evaluation criteria
skate run "Write a product description for wireless headphones." \
  --models gpt-4o,claude-sonnet-4-5,gemini-1.5-pro \
  --judge claude-sonnet-4-5 \
  --judge-criteria "clarity,persuasiveness,brevity"

# Full run: score + judge + export
skate run "How does garbage collection work?" \
  --models gpt-4o,claude-sonnet-4-5 \
  --score \
  --judge gpt-4o \
  --judge-criteria "accuracy,clarity" \
  --output results.csv
