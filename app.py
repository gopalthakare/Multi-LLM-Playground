import gradio as gr

from llm import chat_with_llm
from config import MODELS, API_KEYS


# ------------------------------------
# Generate Response
# ------------------------------------

def generate_response(
    model,
    system_prompt,
    temperature,
    max_tokens,
    prompt,
    history,
):

    if not prompt.strip():

        return (
            "## ⚠️ Empty Prompt\n\nPlease enter a prompt.",
            """
## 📊 Response Statistics

Submit a prompt to view statistics.
""", 
    history,
        )

    answer, stats = chat_with_llm(
        model_name=model,
        system_prompt=system_prompt,
        history=history,
        user_prompt=prompt,
        temperature=temperature,
         max_tokens=max_tokens,
    )

    history.append((prompt, answer))
    return "", answer, stats, history

def clear_chat():
    return "", "", [], "Statistics will appear here."

def provider_status():

    status = []

    providers = {
        "Gemini": "GEMINI_API_KEY",
        "OpenAI": "OPENAI_API_KEY",
        "Anthropic": "ANTHROPIC_API_KEY",
        "Groq": "GROQ_API_KEY",
    }

    for provider, key in providers.items():

        if API_KEYS.get(key):
            status.append(f"🟢 {provider}")
        else:
            status.append(f"🔴 {provider}")

    return "\n".join(status)

# ------------------------------------
# UI
# ------------------------------------

with gr.Blocks(
    title="Multi-LLM Playground",
    theme=gr.themes.Default(
        primary_hue="blue",
        secondary_hue="slate",
    ),
) as app:

    history = gr.State([])
    gr.Markdown(
        """
# 🤖 Multi-LLM Playground

### One Interface • Multiple AI Models

Compare and interact with **Gemini**, **OpenAI**, **Claude**, and **Groq**
through a unified interface powered by **LiteLLM**.
"""
    )

    with gr.Row():

        # -------------------------
        # Left Panel
        # -------------------------

        with gr.Column(scale=1):

            model = gr.Dropdown(
                choices=list(MODELS.keys()),
                value="Gemini 2.5 Flash",
                label="🤖 Select Model",
            )

            system_prompt = gr.Textbox(
                label="📝 System Prompt",
                value="You are a knowledgeable, friendly and concise AI assistant. Respond clearly using Markdown whenever appropriate.",
                lines=5,
            )

            temperature = gr.Slider(
                minimum=0,
                maximum=2,
                value=0.7,
                step=0.1,
                label="🌡 Temperature",
            )

            max_tokens = gr.Slider(
                minimum=100,
                maximum=4096,
                value=1024,
                step=50,
                label="📦 Max Tokens",
            )

            gr.Markdown("### 🔑 Provider Status")
            provider_box = gr.Textbox(
                value=provider_status(),
                interactive=False,
                lines=4,
                label="Available Providers",
            )

        # -------------------------
        # Right Panel
        # -------------------------

        with gr.Column(scale=2):

            prompt = gr.Textbox(
                label="💬 Your Prompt",
                placeholder="Ask anything... e.g. Explain Transformers in simple terms.",
                lines=8,
            )

            submit = gr.Button(
                "✨ Generate",
                variant="primary",
                size="lg",
            )

            clear = gr.Button(
                "🗑 Clear Chat",
            )

            response = gr.Markdown(
                label="🤖 Assistant Response",
            )

            stats = gr.Markdown(
                "Statistics will appear here."
            )

    # -------------------------
    # Button Action
    # -------------------------

    submit.click(
        fn=generate_response,
        inputs=[
            model,
            system_prompt,
            temperature,
            max_tokens,
            prompt,
            history,
        ],
        outputs=[
            prompt,
            response,
            stats,
            history,
        ],
    )

    clear.click(
        fn=clear_chat,
        outputs=[
            prompt,
            response,
            history,
            stats,
        ],
    )

# -------------------------
# Launch App
# -------------------------

if __name__ == "__main__":
    app.launch()