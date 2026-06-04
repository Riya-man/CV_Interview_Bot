# 🤖 AI Resume Interview Bot

An intelligent interview preparation tool that generates customized interview questions based on your resume and evaluates your answers.

## Project Structure

```
CV_Interview_Bot/
├── src/
│   ├── __init__.py
│   ├── server.py              # Main Flask application server
│   └── components/
│       ├── __init__.py
│       ├── resume_parser.py   # PDF resume parsing
│       ├── vector_store.py    # Vector database operations
│       ├── question_generator.py  # AI question generation
│       └── answer_evaluator.py    # AI answer evaluation
├── tests/
│   ├── test.py
│   ├── test_questions.py
│   ├── test_retriever.py
│   └── test_vector.py
├── data/
│   ├── resumes/              # Uploaded resume PDFs
│   └── vector_db/            # Vector database storage
├── outputs/                  # Generated outputs
├── .env                      # Environment variables
├── .gitignore
└── README.md
```

## Features

- 📄 **Resume Parsing**: Extract information from PDF resumes
- 🤖 **Question Generation**: AI-powered interview questions based on resume content
- 📝 **Answer Evaluation**: Intelligent feedback on interview answers
- 🔍 **Context Retrieval**: Vector-based semantic search for relevant resume sections
- 💾 **Vector Storage**: Efficient storage and retrieval of embeddings

## Installation

### Option 1: Local Setup

1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

### Option 2: Docker Setup

1. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

2. **Build and run with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

3. **Access the application**:
   - Open your browser and go to `http://localhost:8501`

## Usage

### Local Development
```bash
python src/server.py
```

### Docker
```bash
docker-compose up
```

Then:
1. Upload your resume (PDF format)
2. Select the interview question type
3. Generate questions based on your resume
4. Answer each question
5. Get AI-powered feedback

## Components

### `resume_parser.py`
Loads and extracts text from PDF resumes using PyPDFLoader.

### `vector_store.py`
Creates and manages vector embeddings for semantic search and retrieval.

### `question_generator.py`
Generates contextual interview questions using LLM based on resume content.

### `answer_evaluator.py`
Evaluates answers and provides constructive feedback.

## Question Types

- Technical
- Project
- HR
- Skills
- Coding Language
- Non-Technical
- Experience
- Achievements

## Testing

Run tests:
```bash
pytest tests/
```

## Requirements

See `requirements.txt` for dependencies. Key packages:
- `flask` - Web framework
- `langchain` - LLM orchestration
- `openai` - LLM API
- `pypdf` - PDF processing

## License

MIT

## Author

Your Name

## Docker Information

### Build and Run
```bash
# Build the Docker image
docker build -t cv-interview-bot .

# Run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f interview-bot

# Stop containers
docker-compose down
```

### Docker Files Included
- **Dockerfile** - Multi-stage Python image with Flask
- **docker-compose.yml** - Service orchestration
- **.dockerignore** - Files excluded from Docker build
- **templates/** - HTML templates for Flask

### Volume Mounts
- `./data/resumes` → `/app/data/resumes` - Resume storage
- `./data/vector_db` → `/app/data/vector_db` - Vector database
- `./outputs` → `/app/outputs` - Generated outputs
- `./src` → `/app/src` - Application code (for development)

### Environment Variables
Copy `.env.example` to `.env` and configure:
```bash
OPENAI_API_KEY=your_key_here
```

### Troubleshooting
- **Port already in use**: Change port in `docker-compose.yml` (8501:8501)
- **Permission denied**: Run with `sudo docker-compose`
- **Out of memory**: Increase Docker memory allocation in settings