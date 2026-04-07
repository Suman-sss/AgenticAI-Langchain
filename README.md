# AgenticAI LangChain Beginner Project

This repository contains a beginner-level agentic AI application built step by step with an industry-style structure.

The goal of this project is not only to make an AI chat app work, but to understand:

- what agentic AI means
- how it differs from plain GenAI and plain RAG
- how UI, API, database, vector database, tools, and orchestration fit together
- why each framework is used
- why we chose some options instead of other options

This project is intentionally built as a learning-first system with production-style architecture.

## Final Use Case

The use case for this beginner project is:

`Agentic Knowledge Assistant`

This assistant can handle three categories of user requests:

1. `Direct answer questions`
   Example: `What is Python?`

2. `Math/tool questions`
   Example: `What is 12 * 8?`

3. `Document or knowledge-base questions`
   Example: `What does the file say about Python?`

This makes the system a good beginner agent because it does not treat every question the same way. It first decides what kind of problem it is solving, and then uses the correct path.

## Why This Is Called Agentic AI

A plain LLM app usually does:

`input -> model -> output`

A plain RAG app usually does:

`input -> retrieve -> model -> output`

This project is more agentic because it does:

`input -> decide route -> use tool or retrieval if needed -> produce final answer`

So the system is not only generating text. It is also making a decision about what action path to follow.

That is the core reason we call it an agentic AI application.

## What The Agent Does

The agent supports three execution paths:

### 1. Direct Path

Used when the question is a normal knowledge or conversational question.

Example:

- `What is Python?`

Action:

- Gemini answers directly

### 2. Tool Path

Used when the question needs deterministic calculation.

Example:

- `What is 12 * 8?`

Action:

- the agent routes to the calculator tool

### 3. Retrieval Path

Used when the question depends on knowledge stored in local files or the vector database.

Example:

- `What does the file say about Python?`

Action:

- retrieve relevant chunks from Chroma
- ask Gemini to answer using only the retrieved context
- show source citations and snippets

## What We Built Step By Step

We built the beginner project in a progression that mirrors good engineering practice.

### Phase 1: Basic Project Structure

We created folders for:

- API
- UI
- agent logic
- tools
- services
- database
- vector store
- prompts
- tests
- docs

Why we did this:

- separation of concerns
- cleaner scaling path
- easier explanation in interviews

Why not put everything in one file:

- would be faster initially
- but much harder to understand, maintain, and extend

### Phase 2: Configuration Layer

We added typed configuration using `pydantic-settings`.

Why:

- central config management
- `.env` support
- cleaner than scattering `os.getenv()` everywhere

Why not only use `os.environ` manually:

- less structured
- more repetitive
- easier to make mistakes

### Phase 3: Database Layer

We added:

- SQLAlchemy session setup
- declarative base
- `ChatMessage` model
- repository layer

Why:

- store conversations in PostgreSQL
- separate persistence from business logic

Why PostgreSQL:

- industry standard
- reliable
- good for structured application data

Why not JSON files for chat history:

- poor queryability
- not production-friendly
- weak backend design for interviews

### Phase 4: API Layer

We built FastAPI routes and schemas.

Why FastAPI:

- typed request and response validation
- auto-generated docs
- modern Python backend framework

Why not Flask:

- Flask is fine, but FastAPI gives better typing and validation for AI backends

### Phase 5: UI Layer

We built a Streamlit chat UI.

Why Streamlit:

- very fast for demos
- minimal frontend complexity
- excellent for beginner AI products

Why not React first:

- more setup
- more frontend overhead
- not needed for a first agentic AI learning project

### Phase 6: Direct LLM Path

We integrated Gemini through LangChain.

Why Gemini:

- free-tier friendly for learning
- strong model capability
- easy official API access

Why through LangChain:

- easier integration with prompts, tools, embeddings, and future agent abstractions

Why not use only raw Google SDK:

- possible, but LangChain gives a smoother path into framework-based agent systems

### Phase 7: Calculator Tool Path

We added a deterministic calculator with safe AST-based parsing.

Why:

- LLMs are not always reliable for exact arithmetic
- tools are a core part of agentic AI

Why not use Python `eval()`:

- unsafe
- can execute arbitrary code

Why AST parsing:

- whitelist-based
- deterministic
- safer for user input

### Phase 8: Retrieval Path

We added:

- embedding service
- Chroma vector store
- retriever tool
- vector ingestion service
- file-based loading from `data/raw`

Why:

- retrieval is essential for grounding answers in external knowledge

Why Chroma:

- easy local setup
- free/open-source
- beginner-friendly

Why not pgvector first:

- pgvector is excellent, but Chroma is simpler for first vector retrieval learning

### Phase 9: Chunking

We added `RecursiveCharacterTextSplitter`.

Why:

- large documents should be split into smaller searchable chunks
- improves retrieval precision

Why not store whole files as one vector:

- weaker retrieval quality
- poor chunk relevance
- harder to scale

### Phase 10: Source Citations

We upgraded responses so retrieval answers include:

- source path
- source snippet

Why:

- trust
- explainability
- better demo quality
- better RAG UX

Why not only show answer text:

- grounded systems should show where the answer came from

### Phase 11: Better Retrieval Quality

We improved vector search by:

- resetting stale collections before re-ingestion
- filtering weak matches with relevance scores

Why:

- avoid stale demo data
- reduce noisy citations

Why not always keep top-k blindly:

- it often introduces weak or irrelevant sources

### Phase 12: Better Agent Routing

We moved from keyword-only routing toward model-based route classification.

Routes:

- `direct`
- `math`
- `retrieval`

Then we improved the route classifier with structured output.

Why:

- more flexible than keywords
- closer to actual agent behavior

Why not keep only keyword routing:

- brittle
- misses natural language phrasing
- less interview-worthy

## Current Architecture

```text
User -> Streamlit UI -> FastAPI API -> Chat Service -> Simple Agent
                                                  |
                                                  |-- direct path -> Gemini
                                                  |-- math path -> calculator tool
                                                  |-- retrieval path -> Chroma retriever -> Gemini
                                                  |
                                                  -> PostgreSQL for chat persistence
```

## Detailed Flow

### Direct Answer Flow

1. User asks a general question in Streamlit
2. FastAPI receives the request
3. Chat service stores the user message in PostgreSQL
4. Agent classifies route as `direct`
5. Gemini answers directly
6. Chat service stores assistant response in PostgreSQL
7. UI shows the answer

### Math Tool Flow

1. User asks a calculation question
2. Agent classifies route as `math`
3. Calculator tool is invoked
4. Deterministic result is returned
5. Result is stored and shown

### Retrieval Flow

1. User asks a document-style question
2. Agent classifies route as `retrieval`
3. Retriever queries Chroma
4. Relevant chunks are returned
5. Gemini receives only grounded context
6. Answer is generated from retrieved content
7. Source path and snippet are shown in UI

## Frameworks Used And Why

### LangChain

Used for:

- Gemini integration
- embeddings
- tools
- structured output
- future transition toward stronger agent abstractions

Why use it:

- common in industry AI apps
- good learning ecosystem
- good bridge from custom logic to framework agents

### FastAPI

Used for:

- backend API
- request/response validation
- clean service architecture

Why use it:

- excellent type support
- clean OpenAPI docs
- common in AI backends

### Streamlit

Used for:

- chat UI
- fast demo experience

Why use it:

- easy for local app demos
- fast iteration
- low frontend complexity

### PostgreSQL

Used for:

- chat storage
- persistent application data

Why use it:

- structured relational data
- very common in production systems

### Chroma

Used for:

- vector storage
- similarity search over document chunks

Why use it:

- easy local vector DB
- great for beginner RAG workflows

### Gemini

Used for:

- route classification
- direct responses
- grounded retrieval responses
- embeddings

Why use it:

- one-provider learning stack
- free-tier friendly
- suitable for both generation and embeddings

## Why We Chose These Options Instead Of Others

### Why not LangGraph yet

LangGraph is excellent for stateful workflows and intermediate-to-advanced orchestration.

We did not start with it because:

- beginner project should teach fundamentals first
- manual routing helps understanding
- too much abstraction too early can hide core concepts

LangGraph is a better fit for the next level.

### Why not CrewAI yet

CrewAI is useful for multi-agent role-based systems.

We did not start there because:

- you first need to understand single-agent routing and tools
- multi-agent design is more advanced

### Why not raw SDK everywhere

Raw SDKs are useful, but we chose LangChain wrappers because:

- they fit the long-term learning path
- they work naturally with tools, structured output, embeddings, and retrievers

### Why not only RAG

This is not only a RAG app because:

- it has a tool path
- it has a direct path
- it has route classification

So retrieval is one capability inside the agent, not the entire system.

## What The Project Demonstrates

This project demonstrates:

- AI application architecture
- agent routing
- tool usage
- RAG
- embeddings
- vector search
- grounded answering
- chat persistence
- frontend/backend integration

## Repository Structure

```text
app/
  agents/
  api/
  core/
  db/
  models/
  prompts/
  repositories/
  schemas/
  services/
  tools/
  ui/
  vectorstore/

data/
  raw/
  processed/

docs/
docker/
scripts/
tests/
```

## How To Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set environment variables in `.env`

Important fields:

```env
PROJECT_NAME=Agentic Beginner
APP_ENV=development
DEBUG=true
API_V1_PREFIX=/api/v1
GOOGLE_API_KEY=your_api_key
GEMINI_MODEL=gemini-2.5-flash
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/agentic_beginner
VECTOR_STORE_PROVIDER=chroma
CHROMA_PERSIST_DIRECTORY=data/processed/chroma
PGVECTOR_COLLECTION_NAME=agentic_knowledge_base
```

### 3. Load files into the vector DB

```bash
./scripts/setup.sh
```

### 4. Run backend

```bash
uvicorn app.main:app --reload
```

### 5. Run UI

```bash
streamlit run app/ui/streamlit_app.py
```

## Example Questions To Test

### Direct path

- `What is Python?`

### Tool path

- `What is 12 * 8?`

### Retrieval path

- `What does the file say about Python?`
- `What does the document say about RAG?`
- `What does the knowledge base say about agentic AI?`

## Current Beginner-Level Outcome

At the end of this beginner project, we have a working single-agent application with:

- route classification
- direct response generation
- tool invocation
- vector retrieval
- grounded answers
- source citations
- UI, API, PostgreSQL, and Chroma integration

This is a strong beginner-level foundation before moving into:

- LangGraph workflows
- more formal tool-calling agents
- file upload ingestion
- multi-agent systems
- advanced observability and evaluation

## What Comes Next

The natural next stage after this beginner project is the intermediate level, where we would typically introduce:

- `LangGraph`
- explicit workflow state
- branching nodes
- better memory/state handling
- more formal orchestration

That would move the system from a beginner routed agent into a more enterprise-style workflow-driven agent.
