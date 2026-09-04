# GitSense

GitSense is an AI-powered repository understanding assistant that helps developers explore unfamiliar GitHub repositories and ask questions about their codebase using natural language.

It combines repository indexing, semantic code search, architecture analysis, web search, and LLM-based tool orchestration to provide context-aware answers.

---

## Features

- **GitHub Repository Indexing**
  - Clone and process GitHub repositories.
  - Build a navigable repository structure.
  - Chunk repository content and generate embeddings.

- **Repository Architecture Analysis**
  - Analyze the indexed repository.
  - Generate information about the repository's purpose, technology stack, entry points, project structure, key modules, and architecture.

- **Semantic Repository Search**
  - Search repository content using natural-language queries.
  - Retrieve relevant code and documentation using vector similarity.

- **AI-Powered Q&A**
  - Ask questions about the repository in natural language.
  - Generate answers using retrieved repository context.

- **Web Search**
  - Use web search for general programming concepts, technologies, libraries, and documentation.

- **Conversation Memory**
  - Maintain conversation history within a chat session for contextual follow-up questions.

- **Repository Explorer**
  - Browse the repository's folder and file structure.
  - Open and inspect individual files.
  - Switch between the repository overview and file view.

---

## Architecture

GitSense uses an agentic RAG architecture in which an orchestrator determines which information sources are required before the final answer is generated.

```text
                         User Question
                              |
                              v
                    +-------------------+
                    |   Orchestrator    |
                    +-------------------+
                              |
                       Tool Selection
                              |
             +----------------+----------------+
             |                |                |
             v                v                v
      Architecture       Repository        Web Search
          Tool              Search             Tool
             |                |                |
             +----------------+----------------+
                              |
                              v
                       Tool Results
                              |
                              v
                    +-------------------+
                    |    Chat Agent     |
                    +-------------------+
                              |
                              v
                        Final Answer


The system separates tool selection and execution from final answer generation.

Orchestrator

The Orchestrator receives the user's question and conversation history and determines which tools are required.

Available tools:

architecture_tool repo_search_tool web_search_tool

The selected tools are executed by the Orchestrator and their results are collected.

### Chat Agent

The Chat Agent receives:

User question Conversation history Tool results

It uses this context to generate the final response.

**RAG** Pipeline

Repository-specific questions use a Retrieval-Augmented Generation pipeline.

GitHub Repository
    |
    v
 Repository Cloning
    |
    v
 File Processing
    |
    v
    Chunking
    |
    v
    Embeddings
    |
    v
 Vector Database
    |
    v
 User Question
    |
    v
 Semantic Retrieval
    |
    v
 Relevant Repository Context
    |
    v
    **LLM**
    |
    v
 Generated Answer

Repository files are divided into smaller chunks and converted into vector embeddings.

When a user asks a repository-specific question, the system retrieves the most relevant chunks and provides them to the Chat Agent as context.

### Repository Architecture Analysis

GitSense also performs high-level analysis of the indexed repository.

The architecture analysis can provide:

Repository purpose Technology stack Entry points Project structure Key modules Architecture patterns

This information is used by the architecture tool when answering high-level repository questions.

### Tool Selection

Different questions can be routed to different tools.

Question Type	Tool
Repository overview	architecture_tool
Specific code or file	repo_search_tool
General programming concept	web_search_tool
Casual conversation	No tool required

For example:

*What is this repository about?*
        ↓
architecture_tool
*How does authentication work?*
        ↓
repo_search_tool
*What is cosine similarity?*
        ↓
web_search_tool
### Tech Stack
Backend
Python
FastAPI
LangChain
GitPython
**FAISS** / vector search
Hugging Face models
Frontend
Next.js
React
Tailwind **CSS**
AI / **RAG**
### Large Language Models
LangChain tool calling
Retrieval-Augmented Generation
Vector embeddings
Semantic search
Conversation memory
### Project Structure
GitSense/
│
├── backend/
│   │
│   ├── agents/
│   │   ├── answer_agent.py
│   │   ├── architecture_agent.py
│   │   ├── chat_agent.py
│   │   └── orchestrator.py
│   │
│   ├── chunking/
│   │   ├── chunker.py
│   │   ├── embedder.py
│   │   └── vectordb.py
│   │
│   ├── retrievers/
│   │   ├── architecture_retriever.py
│   │   ├── repo_retriever.py
│   │   └── web_retriever.py
│   │
│   ├── tools/
│   │   ├── architecture_tool.py
│   │   ├── repo_search.py
│   │   └── web_search.py
│   │
│   ├── executor.py
│   ├── llm.py
│   ├── main.py
│   ├── memory.py
│   ├── prompt_builder.py
│   ├── router.py
│   └── requirements.txt
│
├── frontend/
│   └── repomind/
│       ├── public/
│       ├── src/
│       │   ├── app/
│       │   └── components/
│       ├── package.json
│       └── package-lock.json
│
├── .gitignore
└── **README**.md
### Running Locally
Prerequisites

Make sure the following are installed:

Python Node.js Git npm

You will also need the **API** credentials required by the configured **LLM** provider.

## Clone the repository

git clone <your-repository-url> cd GitSense ## Set up the backend cd backend

Create a virtual environment:

python -m venv .venv

Activate it on Windows:

.venv\Scripts\activate

Install the dependencies:

pip install -r requirements.txt

Create a .env file containing your required **API** key(s).

Example:

OPENROUTER_API_KEY=your_api_key_here

Start the FastAPI server:

uvicorn main:app --reload

The backend will run at:

[http://**127**.0.0.1:**8000**](http://**127**.0.0.1:**8000**) ## Set up the frontend

Open a new terminal:

cd frontend/repomind

Install dependencies:

npm install

Start the development server:

npm run dev

The frontend will normally be available at:

[http://localhost:**3000**](http://localhost:**3000**) **API** Endpoints **POST** /repo

Indexes a GitHub repository.

Request:

{ *repourl*: *[https://github.com/user/repository*](https://github.com/user/repository") }

The endpoint returns the repository tree and architecture information.

**POST** /file-content

Retrieves the contents of a selected repository file.

Request:

{ *path*: */path/to/file.py* } **POST** /search

Processes a user question and returns the generated answer.

Request:

{
    *session_id*: *session-id*,
    *query*: *Explain the repository architecture*
}

Response:

{ *answer*: *...* } ### Example Questions

After indexing a repository, you can ask questions such as:

What is this repository about?

Explain the architecture of this project.

What technologies does this project use?

Where is the main entry point?

Explain how authentication works.

How does this function work?

What does this file do?

How does data flow through this project?

You can also ask general programming questions:

What is cosine similarity?

How does semantic search work?

What is a vector database?

What is Retrieval-Augmented Generation? Security

**API** keys and environment files should never be committed to the repository.

Create a local .env file and keep it excluded through .gitignore.

For example:

OPENROUTER_API_KEY=your_api_key_here

Never replace the placeholder with your real key in a file that will be committed to GitHub.

### Current Limitations

Repository indexing is performed locally. Large repositories may require significant processing time and memory. Binary and unsupported files are not intended for normal text-based retrieval. The current application is primarily designed as a local development and portfolio project. ### Future Improvements

Possible future improvements include:

Better code-aware chunking Improved dependency and call-graph analysis Streaming responses Persistent user accounts and conversations Improved repository caching Support for larger repositories Production deployment More advanced repository visualization ### Project Goal

Understanding an unfamiliar codebase can be difficult when developers have to manually navigate through many files and modules.

GitSense aims to simplify this process by combining:

### Repository Structure

        +
### Semantic Code Search
        +
### Architecture Analysis
        +
### Web Search
        +
**LLM** Reasoning
        =
AI-Powered Repository Understanding
License

This project is intended for educational and portfolio purposes.
