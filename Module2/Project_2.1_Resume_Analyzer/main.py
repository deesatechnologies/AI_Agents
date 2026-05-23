import gradio as gr

from app.llm_service import call_llm
from app.prompts import (
    skill_extraction_prompt,
    resume_job_comparison_prompt,
    candidate_score_prompt,
    interview_questions_prompt,
)


def analyze_resume(resume_text: str, job_description: str) -> str:
    # Validate resume input.
    if not resume_text or not resume_text.strip():
        return "Please paste the candidate resume."

    # Validate job description input.
    if not job_description or not job_description.strip():
        return "Please paste the job description."

    # System prompt defines the overall AI behavior for this project.
    system_prompt = (
        "You are an expert AI recruiting assistant. "
        "Your job is to analyze resumes professionally, clearly, and practically."
    )

    # Step 1: Extract skills from resume.
    skills_result = call_llm(
        system_prompt=system_prompt,
        user_prompt=skill_extraction_prompt(resume_text),
    )

    # Step 2: Compare resume with job description.
    comparison_result = call_llm(
        system_prompt=system_prompt,
        user_prompt=resume_job_comparison_prompt(resume_text, job_description),
    )

    # Step 3: Generate candidate score and recommendation.
    score_result = call_llm(
        system_prompt=system_prompt,
        user_prompt=candidate_score_prompt(resume_text, job_description),
    )

    # Step 4: Generate interview questions.
    questions_result = call_llm(
        system_prompt=system_prompt,
        user_prompt=interview_questions_prompt(resume_text, job_description),
    )

    # Combine all workflow outputs into one final report.
    final_report = f"""
# AI Resume Analysis Report

---

# 1. Skill Extraction

{skills_result}

---

# 2. Resume vs Job Description Comparison

{comparison_result}

---

# 3. Candidate Score and Recommendation

{score_result}

---

# 4. Interview Questions

{questions_result}
"""

    # Return final report to Gradio UI.
    return final_report


with gr.Blocks() as demo:
    # Page title.
    gr.Markdown("# AI Resume Analyzer")

    # Short description for students/users.
    gr.Markdown(
        "Paste a resume and job description. "
        "The AI will analyze skills, gaps, candidate fit, and interview questions."
    )

    # Resume input textbox.
    resume_input = gr.Textbox(
        label="Candidate Resume",
        placeholder="Paste candidate resume here...",
        lines=15,
    )

    # Job description input textbox.
    job_description_input = gr.Textbox(
        label="Job Description",
        placeholder="Paste target job description here...",
        lines=15,
    )

    # Button to trigger analysis.
    analyze_button = gr.Button("Analyze Resume")

    # Markdown output area for the final AI report.
    output = gr.Markdown(label="Resume Analysis Report")

    # When button is clicked, call analyze_resume().
    analyze_button.click(
        fn=analyze_resume,
        inputs=[
            resume_input,
            job_description_input,
        ],
        outputs=output,
    )


if __name__ == "__main__":
    # Launch local Gradio web application.
    demo.launch()