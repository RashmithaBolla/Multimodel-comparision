# Spec — Multi-Model Comparison Tool

## Goal
Ask one question to four LLMs via OpenRouter and show each answer
with its speed and cost, so I can compare models for a real task.

## Input
- A single question (string). Hardcode first; later read from input or web UI.

## Output (per model)
- answer text
- latency (seconds)
- tokens (in/out)
- cost (USD)

## Models (OpenRouter IDs)
- openai/gpt-4o-mini
- anthropic/claude-haiku-4-5
- google/gemini-2.0-flash-001
- meta-llama/llama-3.3-70b-instruct

## Pipeline
1. Load OPENROUTER_API_KEY from .env.
2. For each model: send the question, time the call, read token usage.
3. cost = in_tokens * in_price_per_million / 1_000_000 + out_tokens * out_price_per_million / 1_000_000
4. Print all four results side by side (terminal) or in columns (web UI).

## Error handling
- Wrap each model call in try/except; on failure, log it and continue.
- One model failing must never crash the rest.

## Done when
- One run shows four answers, each with speed and cost.
- One failing model does not stop the others.
- No API key appears in the code or git history.

## Files
- llm.py     — ask() function, MODELS list, PRICES dict (shared engine)
- main.py    — terminal entry point
- app.py     — Streamlit web front-end
- .env       — OPENROUTER_API_KEY (never committed)
- .gitignore — excludes .env, .venv, caches
- requirements.txt — openai, python-dotenv, streamlit
