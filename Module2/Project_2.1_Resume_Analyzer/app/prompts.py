def skill_extraction_prompt(resume_text: str) -> str:
    # This prompt extracts skills from the resume.
    return f"""
You are an expert technical recruiter.

Extract the candidate's skills from the resume below.

Resume:
{resume_text}

Return the result in this format:

## Technical Skills
- skill 1
- skill 2

## Tools and Platforms
- tool 1
- tool 2

## Domain Experience
- domain 1
- domain 2

## Candidate Summary
Write a short summary of the candidate profile.
"""


def resume_job_comparison_prompt(resume_text: str, job_description: str) -> str:
    # This prompt compares the resume against the job description.
    return f"""
You are an expert hiring manager.

Compare the candidate resume with the job description.

Resume:
{resume_text}

Job Description:
{job_description}

Return the result in this format:

## Matching Skills
List skills that match the job description.

## Missing Skills
List important skills missing from the resume.

## Strengths
Explain the candidate's strongest areas.

## Weaknesses
Explain gaps or weak areas.

## Fit Summary
Explain how well the candidate fits the role.
"""


def candidate_score_prompt(resume_text: str, job_description: str) -> str:
    # This prompt generates candidate score and hiring recommendation.
    return f"""
You are an experienced technical recruiter.

Evaluate this candidate for the given job.

Resume:
{resume_text}

Job Description:
{job_description}

Return the result in this format:

## Candidate Score
Give a score from 0 to 100.

## Recommendation
Choose one:
- Strong Match
- Good Match
- Weak Match
- Not Recommended

## Reasoning
Explain why you gave this score.

## Hiring Decision
Should this candidate be shortlisted for interview? Explain clearly.
"""


def interview_questions_prompt(resume_text: str, job_description: str) -> str:
    # This prompt generates interview questions based on resume and job.
    return f"""
You are an expert interviewer.

Generate interview questions for this candidate.

Resume:
{resume_text}

Job Description:
{job_description}

Return the result in this format:

## Technical Questions
Create 5 technical questions.

## Scenario-Based Questions
Create 3 real-world scenario questions.

## Behavioral Questions
Create 3 behavioral questions.

## Skill Gap Questions
Create questions to test missing or weak skills.
"""