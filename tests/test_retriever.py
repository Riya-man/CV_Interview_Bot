from resume_parser import load_resume
from vector_store import create_vector_store
from vector_store import retrieve_context

text = load_resume(
    "resumes/Riya_Mandal(Resume).pdf"
)

index, chunks = create_vector_store(text)

query = "AWS skills"

context = retrieve_context(
    query,
    index,
    chunks
)

print(context)