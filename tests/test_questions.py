from resume_parser import load_resume
from vector_store import create_vector_store
from vector_store import retrieve_context
from question_generator import generate_questions

text = load_resume(
    "resumes/Riya_Mandal(Resume).pdf"
)

index, chunks = create_vector_store(text)

context = retrieve_context(
    "Python AWS Projects",
    index,
    chunks
)

questions = generate_questions(
    context
)

print(questions)