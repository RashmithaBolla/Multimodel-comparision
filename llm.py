"""Shared engine: model list, pricing, and the ask() function."""

import time
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

MODELS = [
    "openai/gpt-4o-mini",
    "anthropic/claude-haiku-4-5",
    "google/gemini-2.0-flash-001",
    "meta-llama/llama-3.3-70b-instruct",
]

# Price per million tokens (input, output) in USD — check openrouter.ai for live rates
PRICES = {
    "openai/gpt-4o-mini":                  (0.15,  0.60),
    "anthropic/claude-haiku-4-5":          (0.80,  4.00),
    "google/gemini-2.0-flash-001":         (0.10,  0.40),
    "meta-llama/llama-3.3-70b-instruct":   (0.065, 0.065),
}


def _client() -> OpenAI:
    key = os.getenv("OPENROUTER_API_KEY")
    if not key:
        raise EnvironmentError("OPENROUTER_API_KEY not found. Add it to your .env file.")
    return OpenAI(api_key=key, base_url="https://openrouter.ai/api/v1")


def ask(question: str, model: str) -> dict:
    """
    Send *question* to *model* via OpenRouter.

    Returns a dict with keys:
        model, answer, latency, input_tokens, output_tokens, cost, error
    On failure, answer is None and error holds the exception message.
    """
    result = {
        "model": model,
        "answer": None,
        "latency": None,
        "input_tokens": 0,
        "output_tokens": 0,
        "cost": None,
        "error": None,
    }

    try:
        client = _client()
        start = time.perf_counter()
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": question}],
            timeout=30,
        )
        result["latency"] = round(time.perf_counter() - start, 2)

        result["answer"] = response.choices[0].message.content

        usage = response.usage
        if usage:
            result["input_tokens"] = usage.prompt_tokens or 0
            result["output_tokens"] = usage.completion_tokens or 0

        in_price, out_price = PRICES.get(model, (0, 0))
        result["cost"] = (
            result["input_tokens"] * in_price / 1_000_000
            + result["output_tokens"] * out_price / 1_000_000
        )

    except Exception as exc:
        result["error"] = str(exc)

    return result
