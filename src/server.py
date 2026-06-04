from flask import Flask, request, render_template, redirect, url_for, session
from werkzeug.utils import secure_filename
from components.resume_parser import load_resume
from components.vector_store import create_vector_store, retrieve_context
from components.question_generator import generate_questions
from components.answer_evaluator import evaluate_answer
from pathlib import Path
from uuid import uuid4
import os

BASE_DIR = Path(__file__).parent.parent
app = Flask(__name__, template_folder=str(BASE_DIR / "templates"))
app.secret_key = os.environ.get("SECRET_KEY", "local_dev_secret")
DATA_DIR = BASE_DIR / "data" / "resumes"
DATA_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {"pdf"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET"])
def index():
    categories = [
        "Technical",
        "Project",
        "HR",
        "SKILLS",
        "Coding Language",
        "Non-Technical",
        "Experience",
        "Achievements",
    ]
    return render_template("index.html", categories=categories)


@app.route("/generate", methods=["POST"])
def generate():
    uploaded_file = request.files.get("resume")
    category = request.form.get("category")
    resume_file = session.get("resume_file")

    if uploaded_file and uploaded_file.filename != "":
        if not allowed_file(uploaded_file.filename):
            return "Invalid file type", 400

        filename = f"uploaded_resume_{uuid4().hex}.pdf"
        file_path = DATA_DIR / filename
        uploaded_file.save(file_path)
        session["resume_file"] = filename
        session["resume_name"] = secure_filename(uploaded_file.filename)
    elif resume_file:
        file_path = DATA_DIR / resume_file
    else:
        return "No file uploaded", 400

    if not file_path.exists():
        return "Resume file not found", 400

    text = load_resume(str(file_path))
    index, chunks = create_vector_store(text)
    context = retrieve_context(category, index, chunks)
    questions_text = generate_questions(context, category)

    question_list = [
        q.strip()
        for q in questions_text.split("\n")
        if q.strip() and (q[0].isdigit() or q.startswith("-"))
    ]

    if not question_list:
        question_list = [questions_text]

    session["questions"] = question_list
    session["current_index"] = 0
    session["category"] = category

    return redirect(url_for("question"))


@app.route("/question", methods=["GET"])
def question():
    questions = session.get("questions")
    current_index = session.get("current_index", 0)

    if not questions or current_index >= len(questions):
        return redirect(url_for("index"))

    question_text = questions[current_index]
    return render_template(
        "questions.html",
        question=question_text,
        index=current_index,
        total=len(questions),
    )


@app.route("/category", methods=["GET"])
def category():
    if not session.get("resume_file"):
        return redirect(url_for("index"))

    categories = [
        "Technical",
        "Project",
        "HR",
        "SKILLS",
        "Coding Language",
        "Non-Technical",
        "Experience",
        "Achievements",
    ]
    return render_template(
        "category.html",
        categories=categories,
        resume_name=session.get("resume_name"),
    )


@app.route("/evaluate", methods=["POST"])
def evaluate():
    index = request.form.get("index")
    answer = request.form.get("answer")
    questions = session.get("questions")

    if index is None or answer is None:
        return "Missing question or answer", 400

    try:
        current_index = int(index)
    except ValueError:
        return "Invalid question index", 400

    if not questions or current_index >= len(questions):
        return redirect(url_for("index"))

    question_text = questions[current_index]
    feedback = evaluate_answer(question_text, answer)

    next_index = current_index + 1
    has_next = next_index < len(questions)

    if has_next:
        session["current_index"] = next_index
    else:
        session.pop("questions", None)
        session.pop("current_index", None)
        session.pop("category", None)

    return render_template(
        "feedback.html",
        question=question_text,
        answer=answer,
        feedback=feedback,
        has_next=has_next,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8501, debug=True)
