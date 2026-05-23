import gradio as gr

from app.research_assistant import generate_research_summary


def research_topic(topic: str) -> str:
    """
    This function runs when the user clicks the button in the UI.
    """

    if not topic or not topic.strip():
        return "Please enter a topic to research."

    return generate_research_summary(topic)

#create the demo interface using gr.Interface
demo = gr.Interface(
    fn=research_topic, #when the user interacts with the UI,call this function
    inputs=gr.Textbox(
        label="Enter a topic",
        placeholder="Example: What is an AI Agent?",
        lines=2,
    ),
    outputs=gr.Markdown(label="Research Summary"),
    title="AI Research Assistant", #title of the interface
    description=(
        "Enter any topic and the AI will generate a beginner-friendly "
        "structured research summary."
    ),
)


if __name__ == "__main__":
    demo.launch()