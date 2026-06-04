from langchain_community.document_loaders import PyPDFLoader

def load_resume(pdf_path):
    loader = PyPDFLoader(pdf_path)

    docs = loader.load()

    text = ""

    for doc in docs:
        text += doc.page_content + "\n"

    return text