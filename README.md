# Enterprise Knowledge Intelligence Platform

An enterprise-grade GenAI and Agentic AI platform designed to demonstrate production-oriented backend engineering, Retrieval-Augmented Generation (RAG), intelligent agents, and enterprise knowledge processing.

The project is being developed incrementally as an interview-ready portfolio project for Senior GenAI Engineer roles.

## Current Status

**Stage 11 — MCP Integration & Enterprise Tooling: Complete**

Implemented and verified:

* Python 3.13
* `uv` package manager
* FastAPI application
* Health check endpoint
* Pydantic Settings configuration
* Environment-based configuration
* PostgreSQL
* SQLAlchemy 2.x Async
* `asyncpg`
* Async database sessions
* Alembic migrations
* Document ingestion and processing
* Embedding generation
* Azure OpenAI integration
* Azure AI Search integration
* RAG pipeline
* LangGraph agent workflows
* Retrieval and SQL tools
* SQL guardrails
* Sensitive-data classification
* Human-in-the-loop approval
* Redis Docker infrastructure
* Redis service layer
* Redis integration testing
* Agent response caching
* Redis-backed API rate limiting
* Request ID propagation
* Request duration logging
* LLM error handling
* Agent error handling
* Redis failure fallback
* Destructive SQL protection
* Sensitive-data access protection
* Docker verification
* Pytest
* Ruff

### Verification

* 111 tests passed
* Ruff checks passed
* Docker API verified
* `/health` endpoint verified
* Agent query endpoint verified
* Sensitive-data HITL verified
* Destructive operation blocking verified

## Technology Stack

### Backend

* Python 3.13
* FastAPI
* SQLAlchemy Async
* PostgreSQL
* Alembic
* Pydantic Settings

### Testing & Code Quality

* pytest
* pytest-asyncio
* Ruff

### GenAI & AI Engineering

* RAG (Retrieval-Augmented Generation)
* Agentic AI
* LangGraph
* Azure OpenAI
* Azure AI Search
* Enterprise Retrieval
* SQL Agent
* Prompt-driven workflows
* Model Context Protocol (MCP)
* Streamable HTTP

### Security & Reliability

* HITL (Human-in-the-Loop)
* SQL Guardrails
* Sensitive-data protection
* Destructive operation protection
* Redis caching
* Rate Limiting
* Failure fallback
* LLM failure handling
* Agent failure handling
* Request ID tracking
* Structured logging

### Testing & Quality

* pytest
* pytest-asyncio
* API testing
* Agent testing
* RAG/retrieval testing
* Redis integration testing
* Regression testing
* Ruff

## Project Architecture

The platform is built around a production-oriented GenAI architecture combining RAG, Agentic AI, security guardrails, human approval, caching, rate limiting, failure handling, and observability.

```text
Enterprise Knowledge Intelligence Platform
│
├── FastAPI Backend
│
├── PostgreSQL
│
├── Document Ingestion & Processing
│
├── RAG Pipeline
│   ├── Document Retrieval
│   ├── Context Building
│   ├── Azure AI Search
│   └── Azure OpenAI
│
├── Agentic AI
│   ├── LangGraph Workflows
│   ├── Action Classification
│   ├── Retrieval Tool
│   └── SQL Tool
│
│
├── Model Context Protocol (MCP)
│   ├── Streamable HTTP MCP Server
│   ├── Knowledge Search Tool
│   └── Read-Only SQL Tool
│
├── Security & Guardrails
│   ├── SQL Guardrails
│   ├── Read-Only SQL Enforcement
│   ├── Sensitive-Data Protection
│   ├── Destructive Operation Protection
│   └── HITL (Human-in-the-Loop)
│
├── Reliability & Performance
│   ├── Redis Response Caching
│   ├── Rate Limiting
│   ├── Cache Failure Fallback
│   ├── Rate-Limiter Failure Fallback
│   ├── LLM Failure Handling
│   └── Agent Failure Handling
│
└── Observability
    ├── Request ID Tracking
    ├── Request Duration Logging
    └── Structured Error Logging

``` 

## Project Structure

```text
enterprise-knowledge-intelligence-platform/
│
├── app/
│   ├── api/
│   ├── agents/
│   │   └── tools/
│   ├── mcp/
│   │   └── server.py
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   ├── repositories/
│   └── services/
│
├── alembic/
│   └── versions/
│
├── tests/
│   ├── agents/
│   ├── api/
│   ├── integration/
│   └── services/
│
├── .env.example
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── README.md
└── uv.lock
```

## Local Development

## MCP Server

The platform exposes selected enterprise capabilities through the Model Context Protocol (MCP).

The MCP server reuses the existing application services rather than implementing a separate retrieval or SQL layer.

### Start the MCP server

```bash
uv run python -m app.mcp.server

### Requirements

* Python 3.13
* uv
* PostgreSQL
* Docker / Docker Compose

### Install dependencies

```bash
uv sync
```

### Configure environment

Create a local `.env` file based on `.env.example`.

```bash
cp .env.example .env
```

Update the local database configuration and any required service credentials.

**Never commit `.env` or production secrets to Git.**

### Run database migrations

```bash
uv run alembic upgrade head
```

### Run the application

```bash
uv run uvicorn app.main:app --reload
```

### Run tests

```bash
uv run pytest
```

### Run Ruff

```bash
uv run ruff check .
```

```bash
uv run ruff format .
```

## Database

The current development database uses PostgreSQL with asynchronous SQLAlchemy sessions.

Current migration head:

```bash
86ff295bd3c7
```

Verify the current migration:

```bash
uv run alembic current
```

## Development Roadmap

### Stage 1 — Project Foundation

Implemented:

* Python 3.13 project setup
* `uv` package manager
* FastAPI application foundation
* Application configuration
* Pydantic Settings
* Environment-based configuration
* Health check endpoint
* Basic project structure
* Pytest configuration
* Ruff configuration
* Git repository setup

**Status: Complete**

### Stage 2 — Backend & Database Foundation

Implemented:

* PostgreSQL database
* SQLAlchemy 2.x Async
* `asyncpg`
* Async database sessions
* Database dependency injection
* User database model
* Alembic configuration
* Database migrations
* Initial migration workflow
* Database integration tests

**Status: Complete**

### Stage 3 — Enterprise Document Ingestion

Implemented:

* Document upload API
* File validation
* Document metadata
* Document persistence
* Document parsing
* PDF document processing
* DOCX document processing
* Text extraction
* Document chunking
* Document processing service
* Persistent document lifecycle
* Document processing tests

**Status: Complete**

### Stage 4 — Embeddings & Vector Search

Implemented:

* Local embedding generation
* Sentence Transformer integration
* Embedding service abstraction
* Vector search foundations
* PostgreSQL vector storage
* Retrieval service
* Vector search service
* Embedding and retrieval tests

**Status: Complete**

### Stage 5 — RAG Pipeline

Implemented:

* Azure OpenAI integration
* Azure AI Search integration
* Knowledge retrieval
* Context building
* RAG pipeline
* Retrieval service
* Context generation
* LLM response generation
* RAG service tests
* Azure service tests

**Status: Complete**

### Stage 6 — Agentic AI

Implemented:

* LangGraph agent workflow
* Agent graph
* Agent nodes
* Agent state management
* Retrieval tool
* SQL tool
* SQL agent
* Agent execution service
* Action classification
* Agent API
* Agent service tests
* Agent graph tests
* Agent node tests
* Tool tests

**Status: Complete**

### Stage 7 — Security, Guardrails & Human-in-the-Loop

Implemented:

* SQL guardrails
* Read-only SQL enforcement
* Destructive SQL protection
* Multiple SQL statement protection
* Sensitive column detection
* Sensitive-data classification
* Human-in-the-loop approval
* Approval status handling
* Sensitive-data access protection
* SQL security tests
* HITL tests
* API security tests

**Status: Complete**

### Stage 8 — Production Backend Integration

Implemented:

* Production-oriented FastAPI API layer
* Agent query API
* Request validation
* Centralized application exceptions
* LLM error handling
* Agent execution error handling
* API error handlers
* Request ID generation
* Request ID propagation
* Dockerfile
* Docker Compose
* PostgreSQL container
* API container
* Integration testing
* API testing
* Health endpoint testing

**Status: Complete**

### Stage 9 — Production Reliability, Rate Limiting, Caching & Observability

Implemented:

* Redis Docker infrastructure
* Redis service layer
* Redis integration testing
* Agent response caching
* Normalized cache keys
* SHA-256 cache keys
* Configurable cache TTL
* Redis-backed API rate limiting
* Configurable rate-limit window
* Request ID tracking
* Request duration measurement
* Structured request logging
* LLM failure handling
* Agent failure handling
* Redis cache failure fallback
* Redis rate-limiter failure fallback
* Sensitive-data protection
* Destructive operation blocking
* Production Docker verification
* Full regression testing

**Status: Complete**

### Stage 10 — Final Production Readiness

Implemented:

* Production deployment architecture
* Kubernetes / AKS readiness
* CI/CD pipeline
* Production observability
* Performance optimization
* Load testing
* Deployment documentation
* Final architecture documentation
* Final portfolio cleanup

**Status: Complete**

**Stage 11 — MCP Integration & Enterprise Tooling: Complete**

Implemented:

* Model Context Protocol (MCP) server
* Streamable HTTP MCP transport
* Enterprise knowledge search MCP tool
* Read-only SQL MCP tool
* MCP tool integration with existing retrieval and SQL services

**Status: Complete**

## Engineering Goals

This project emphasizes production engineering rather than a simple chatbot implementation.

Key engineering concerns include:

* Clean architecture
* Async backend design
* Database reliability
* Testability
* Configuration management
* Secret management
* RAG quality
* Agent reliability
* Observability
* Security
* Scalability
* Performance
* Failure handling
* Production deployment

## License

This project is currently intended as a personal engineering and interview portfolio project.
