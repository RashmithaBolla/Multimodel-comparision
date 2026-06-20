# Multi-Model Comparison Tool

Ask one question to four LLMs via OpenRouter and compare answers, speed and cost.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Mac / Linux

pip install -r requirements.txt
```

Add your OpenRouter key to `.env`:

```
OPENROUTER_API_KEY=sk-or-...your key here...
```

## Run (terminal)

```bash
python main.py
# or pass a custom question:
python main.py "What is the difference between RAM and a hard drive?"
```

## Run (web UI)

```bash
streamlit run app.py
```

Then open <http://localhost:8501> in your browser.

## Project structure

```
multimodel-v2-app/
├─ .env              ← your OpenRouter API key  (never committed)
├─ .gitignore
├─ spec.md           ← specification written before code
├─ requirements.txt
├─ llm.py            ← shared engine: ask(), MODELS, PRICES
├─ main.py           ← terminal entry point
├─ app.py            ← Streamlit web front-end
└─ README.md
```
