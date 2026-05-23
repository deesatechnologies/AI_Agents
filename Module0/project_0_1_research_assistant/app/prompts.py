def build_research_prompt(topic: str) -> str:
   

    return f"""
You are an expert teacher and research assistant.

Explain the following topic in a beginner-friendly way:

Topic: {topic}

Please use this exact structure:

1. Short Summary
Explain the topic in 3 to 5 simple lines.

2. Beginner Explanation
Explain it as if the student is completely new.

3. Key Concepts
List the most important concepts related to this topic.

4. Real-World Example
Give one practical example from real life or industry.

5. Why This Matters
Explain why students or professionals should care about this topic.

6. Common Confusion
Mention one common misunderstanding beginners may have.

Keep the language simple, clear, and practical.
"""