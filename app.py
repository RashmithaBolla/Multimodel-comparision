"""Streamlit web front-end for the Multi-Model Comparison Tool."""

import streamlit as st
from llm import ask, MODELS, PRICES

st.set_page_config(page_title="Multi-Model Comparison Tool", layout="wide")

st.title("Multi-Model Comparison Tool")
st.caption(
    "Ask one question — see four models answer side by side with speed and cost. "
    "Prices are illustrative; check [OpenRouter](https://openrouter.ai) for live rates."
)

# ── Inputs ────────────────────────────────────────────────────────────────────

question = st.text_area(
    "Your question",
    placeholder="e.g. Explain quantum entanglement in one sentence.",
    height=100,
)

selected_models = st.multiselect(
    "Models to compare",
    options=MODELS,
    default=MODELS,
)

compare_clicked = st.button("Compare models", type="primary", disabled=not selected_models)

# ── Run ───────────────────────────────────────────────────────────────────────

if compare_clicked:
    if not question.strip():
        st.warning("Please enter a question before clicking Compare.")
        st.stop()

    results = {}
    with st.spinner("Querying models — this may take up to 30 seconds…"):
        for model in selected_models:
            results[model] = ask(question.strip(), model)

    # ── Results ───────────────────────────────────────────────────────────────

    st.divider()
    cols = st.columns(len(selected_models))

    for col, model in zip(cols, selected_models):
        r = results[model]
        short_name = model.split("/")[-1]

        with col:
            st.subheader(short_name)

            if r["error"]:
                st.error(f"**Error:** {r['error']}")
            else:
                st.write(r["answer"])
                st.metric("Latency", f"{r['latency']} s")
                st.metric(
                    "Cost (est.)",
                    f"${r['cost']:.5f}",
                    help=f"Input tokens: {r['input_tokens']}  |  Output tokens: {r['output_tokens']}",
                )
