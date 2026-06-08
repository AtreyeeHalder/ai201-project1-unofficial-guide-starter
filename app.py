"""Query interface — Gradio web UI

Pipeline stage covered here:

    user query --(Gradio)--> answer_query() --> grounded answer + sources

This is a thin presentation layer. Here we collect a question, call the pipeline, and
render the returned markdown (answer + programmatically-attached source list).

Run:  python app.py   then open the printed local URL.
"""

from __future__ import annotations

import gradio as gr

from generator import answer_query

# Drawn from the Evaluation Plan in planning.md so reviewers can test instantly.
EXAMPLE_QUERIES = [
    "When is Hoboken street parking free?",
    "What is the walk score of Hoboken?",
    "How much does the Stevens shuttle cost?",
    "Will changing from dorming to commuting affect my financial aid?",
    "What are the downsides of parking with a temporary Hoboken pass?",
]

DESCRIPTION = (
    "Ask about the **commuter experience at Stevens Institute of Technology**: "
    "parking, transit, dorming vs. commuting, safety, and more. Answers are "
    "grounded **only** in unofficial sources such as Reddit threads (mostly), "
    "Apartments.com, and walkscore.com, and every answer lists the documents "
    "it came from. If the sources don't cover your question, the guide is "
    "designed to say so rather than guess."
)


LOADING_MESSAGE = "⏳ Searching the guide and generating a grounded answer…"


def respond(question: str):
    """Gradio callback (a generator, so the UI can show a loading state).

    Yields twice per call: first an immediate "generating" message (with the
    Ask button disabled to block double-submits), then the final grounded
    answer once answer_query() returns. Each yield is (answer_markdown,
    ask_button_update) to match the two output components.
    """
    if not question or not question.strip():
        yield "Please enter a question.", gr.update(interactive=True, value="Ask")
        return

    # First yield: show the loading message right away and lock the button.
    yield LOADING_MESSAGE, gr.update(interactive=False, value="Generating…")

    try:
        result = answer_query(question.strip())
    except Exception as exc:  # surface config/runtime issues in the UI, don't crash
        result = f"Something went wrong while answering: {exc}"

    # Second yield: the real answer, button re-enabled.
    yield result, gr.update(interactive=True, value="Ask")


def build_ui() -> gr.Blocks:
    """Assemble the Gradio Blocks app."""
    with gr.Blocks(title="The Unofficial Guide — Stevens Commuters") as demo:
        gr.Markdown("# 🚆 The Unofficial Guide — Stevens Commuters")
        gr.Markdown(DESCRIPTION)

        with gr.Row():
            question = gr.Textbox(
                label="Your question",
                placeholder="e.g. When is Hoboken street parking free?",
                lines=2,
                scale=4,
                autofocus=True,
            )
        with gr.Row():
            ask_btn = gr.Button("Ask", variant="primary")
            clear_btn = gr.ClearButton(value="Clear")

        answer = gr.Markdown(label="Answer")

        gr.Examples(examples=EXAMPLE_QUERIES, inputs=question, label="Try a question")

        # Wire it all together: button click and Enter both run the pipeline.
        # outputs include ask_btn so respond() can disable it while generating.
        ask_btn.click(fn=respond, inputs=question, outputs=[answer, ask_btn])
        question.submit(fn=respond, inputs=question, outputs=[answer, ask_btn])
        clear_btn.add([question, answer])

    return demo


def main() -> None:
    build_ui().launch()


if __name__ == "__main__":
    main()
