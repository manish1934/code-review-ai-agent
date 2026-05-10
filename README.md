# Code Review AI Agent

A production-ready multi-agent system that performs automated code review using **GenAI + RAG** architecture.

## Architecture

```
User Code Input
      ↓
Supervisor Agent (LangChain + Llama 3)
   ↙      ↓       ↘
Bug     Security   Optimizer
Detector Analyst   Agent
   ↘      ↓       ↙
     RAG Pipeline
  (ChromaDB + Embeddings)
      ↓
 Final Review Report
```

## Tech Stack

| Component | Technology |
|-----------|-----------|
| LLM | Groq (Llama 3 70B) — FREE |
| Orchestration | LangChain |
| Vector DB | ChromaDB |
| Embeddings | Sentence Transformers (local, free) |
| Evaluation | RAGAS metrics |
| UI | Streamlit |

## Setup (5 minutes)

### 1. Clone and navigate
```bash
git clone <your-repo-url>
cd code-review-agent
```

### 2. Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Get free Groq API key
- Go to https://console.groq.com
- Sign up (free, no credit card)
- Create an API key

### 5. Set up environment
```bash
cp .env.example .env
# Edit .env and paste your GROQ_API_KEY
```

### 6. Run the app
```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser.

## Project Structure

```
code-review-agent/
├── agents/
│   ├── supervisor.py       # Orchestrates all agents
│   ├── bug_detector.py     # Finds logic errors
│   ├── security_analyst.py # OWASP security checks
│   └── optimizer.py        # Performance improvements
├── rag/
│   ├── ingest.py           # Load + chunk + embed docs
│   ├── retriever.py        # Query ChromaDB
│   └── knowledge_base/     # Add your PDFs/docs here
├── memory/
│   └── memory_manager.py   # Session history
├── eval/
│   └── ragas_eval.py       # Quality evaluation
├── app.py                  # Streamlit UI
├── requirements.txt
└── .env.example
```

## Adding Custom Knowledge

Drop any `.txt` or `.pdf` files into `rag/knowledge_base/` and the RAG pipeline will automatically index them on next startup.

Examples to add:
- Your company's coding standards
- PEP8 full documentation PDF
- OWASP Top 10 PDF
- Language-specific style guides

## Resume Points

```
Code Review AI Agent | Python, LangChain, RAG, Groq Llama 3
- Built a multi-agent system with 3 specialist agents (Bug Detector,
  Security Analyst, Code Optimizer) orchestrated by a Supervisor agent
- Implemented RAG pipeline using ChromaDB vector store with
  Sentence Transformers embeddings over coding best practices corpus
- Achieved automated OWASP vulnerability detection and PEP8 compliance
  checking using retrieval-augmented generation
- Evaluated output quality using RAGAS metrics (relevancy, coverage,
  completeness)
```
