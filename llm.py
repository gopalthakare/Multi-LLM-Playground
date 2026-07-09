import time
import litellm

from config import MODELS


def chat_with_llm(
    model_name: str,
    system_prompt: str,
    history: list,
    user_prompt: str,
    temperature: float,
    max_tokens: int,
):
    """
    Sends a prompt to the selected LLM while preserving chat history.
    """

    model = MODELS[model_name]

    # Build message history
    messages = [
        {
            "role": "system",
            "content": system_prompt,
        }
    ]

    # Previous conversation
    for user, assistant in history:
        messages.append(
            {
                "role": "user",
                "content": user,
            }
        )

        messages.append(
            {
                "role": "assistant",
                "content": assistant,
            }
        )

    # Current prompt
    messages.append(
        {
            "role": "user",
            "content": user_prompt,
        }
    )

    try:

        start = time.perf_counter()

        response = litellm.completion(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        end = time.perf_counter()

        answer = response.choices[0].message.content

        latency = round(end - start, 2)

        prompt_tokens = response.usage.prompt_tokens
        completion_tokens = response.usage.completion_tokens
        total_tokens = response.usage.total_tokens

        cost = response._hidden_params.get("response_cost") or 0

        stats = f"""
## 📊 Response Statistics

- ⚡ **Response Time:** {latency:.2f}s

- 🪙 **Prompt Tokens:** {prompt_tokens}

- 🤖 **Completion Tokens:** {completion_tokens}

- 📦 **Total Tokens:** {total_tokens}

- 💰 **Estimated Cost:** ${cost:.6f}
"""

        return answer, stats

    except Exception as e:

        return (
            f"❌ Error:\n\n{e}",
            "No statistics available."
        )