from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def evaluate_answer(question, answer):

    prompt = f"""
Question:
{question}

Answer:
{answer}

Evaluate the answer.

Give:
1. Score out of 10
2. Strengths
3. Weaknesses
4. Missing Concepts
5. Improved Answer
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content
