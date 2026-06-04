from resume_parser import load_resume
from vector_store import create_vector_store

text = load_resume("resumes/Riya_Mandal(Resume).pdf")

index, chunks = create_vector_store(text)

print("Number of Chunks:", len(chunks))
print()
print("First Chunk:")
print(chunks[0])