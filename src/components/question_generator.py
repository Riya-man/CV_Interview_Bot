from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_questions(context,category):

    prompt = f"""
    You are an experienced technical interviewer.

    Question Category: {category}


    Resume Context:
    {context}

    Generate 10 interview questions specifically related to {category}.

    If category is:
    - Technical → technical questions
    - Project → project-based questions
    - HR → HR questions
    - AWS → AWS-focused questions
    - Python → Python-focused questions
    - Machine Learning → ML-focused questions
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]
    )

    return response.choices[0].message.content