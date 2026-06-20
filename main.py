"""Terminal entry point for the Multi-Model Comparison Tool."""

from llm import ask, MODELS

QUESTION = "Explain what a large language model is in two sentences, as if speaking to a 10-year-old."


def run(question: str) -> None:
    print(f"\nQuestion: {question}\n")
    print("=" * 72)

    results = [ask(question, model) for model in MODELS]

    # Column widths
    col = 17
    bar = "-" * 72

    # Header row
    headers = [r["model"].split("/")[-1][:col] for r in results]
    print("  ".join(h.ljust(col) for h in headers))
    print(bar)

    # Answer preview (word-wrap at col chars per column)
    max_preview = 120
    for r in results:
        text = r["error"] or r["answer"] or ""
        preview = (text[:max_preview] + "…") if len(text) > max_preview else text
        # Break into col-wide chunks
        chunks = [preview[i:i+col] for i in range(0, len(preview), col)]
        if not chunks:
            chunks = [""]
        # Print alongside other columns (simplified: one block per result)
        print(preview[:col].ljust(col), end="  ")
    print()

    # Print remaining lines of each preview
    previews = []
    for r in results:
        text = r["error"] or r["answer"] or ""
        preview = (text[:max_preview] + "…") if len(text) > max_preview else text
        lines = [preview[i:i+col] for i in range(0, len(preview), col)]
        previews.append(lines)

    max_lines = max(len(p) for p in previews)
    for line_idx in range(1, max_lines):
        for p in previews:
            cell = p[line_idx] if line_idx < len(p) else ""
            print(cell.ljust(col), end="  ")
        print()

    print(bar)

    # Stats row
    for r in results:
        if r["error"]:
            stat = "ERROR"
        else:
            stat = f"{r['latency']}s  ${r['cost']:.5f}"
        print(stat.ljust(col), end="  ")
    print("\n")


if __name__ == "__main__":
    import sys
    question = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else QUESTION
    run(question)
