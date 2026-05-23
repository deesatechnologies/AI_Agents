import gradio as gr
from openai import OpenAI

from app.config import (
    get_model_provider,
    get_openai_api_key,
    get_openai_model,
    get_deepseek_api_key,
    get_deepseek_model,
)


def get_client_and_model():
    # Read provider from .env file.
    provider = get_model_provider()

    # If provider is OpenAI, create OpenAI client.
    if provider == "openai":
        client = OpenAI(api_key=get_openai_api_key())
        model = get_openai_model()
        return client, model, provider

    # If provider is DeepSeek, create DeepSeek client.
    # DeepSeek uses OpenAI-compatible API format.
    if provider == "deepseek":
        client = OpenAI(
            api_key=get_deepseek_api_key(),
            base_url="https://api.deepseek.com",
        )
        model = get_deepseek_model()
        return client, model, provider

    # If provider is not supported, stop program with clear error.
    raise ValueError("Unsupported MODEL_PROVIDER. Use 'openai' or 'deepseek'.")


def format_chat_history(history):
    # Convert conversation history into readable Markdown text.
    if not history:
        return "No conversation yet."

    markdown_text = ""

    for message in history:
        role = message["role"]
        content = message["content"]

        if role == "user":
            markdown_text += f"### You\n{content}\n\n"
        elif role == "assistant":
            markdown_text += f"### Assistant\n{content}\n\n"

    return markdown_text


def chat_with_ai(user_message, history):
    # If history is None, initialize it as an empty list.
    if history is None:
        history = []

    # If user sends empty message, do not call API.
    if not user_message or not user_message.strip():
        return "", format_chat_history(history), history

    # Create client and select model.
    client, model, provider = get_client_and_model()

    print(f"\nUsing provider: {provider}")
    print(f"Using model: {model}")

    # System message defines chatbot behavior.
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful AI assistant. "
                "Explain concepts clearly and simply."
            ),
        }
    ]

    # Add previous messages so the model has conversation context.
    messages.extend(history)

    # Add current user message.
    messages.append(
        {
            "role": "user",
            "content": user_message,
        }
    )

    # Send messages to selected AI model.
    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )

    # Extract assistant reply.
    assistant_response = response.choices[0].message.content

    print("\n=== TOKEN USAGE ===")
    print("Prompt Tokens:", response.usage.prompt_tokens)
    print("Completion Tokens:", response.usage.completion_tokens)
    print("Total Tokens:", response.usage.total_tokens)

    # Save user message into history.
    history.append(
        {
            "role": "user",
            "content": user_message,
        }
    )

    # Save assistant response into history.
    history.append(
        {
            "role": "assistant",
            "content": assistant_response,
        }
    )

    # Clear textbox, update markdown chat display, and update hidden state.
    return "", format_chat_history(history), history


def clear_conversation():
    # Clear textbox, visible chat history, and hidden conversation state.
    return "", "No conversation yet.", []


with gr.Blocks() as demo:
    gr.Markdown("# AI Chatbot (Basic)")

    gr.Markdown(
        "Ask questions and chat with the AI assistant. "
        "This version uses Markdown chat history to avoid Gradio version issues."
    )

    chat_display = gr.Markdown(
        value="No conversation yet.",
        label="Conversation",
    )

    user_input = gr.Textbox(
        label="Your Message",
        placeholder="Ask anything...",
        lines=2,
    )

    send_button = gr.Button("Send")
    clear_button = gr.Button("Clear Conversation")

    state = gr.State([])

    send_button.click(
        fn=chat_with_ai,
        inputs=[user_input, state],
        outputs=[user_input, chat_display, state],
    )

    clear_button.click(
        fn=clear_conversation,
        outputs=[user_input, chat_display, state],
    )


if __name__ == "__main__":
    demo.launch()