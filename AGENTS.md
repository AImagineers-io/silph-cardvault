# AGENT.md

This file defines the coding standards, structure, and expectations for contributors, collaborators, and AI agents working on the `silph-cardvault` microservice.
Everything here is intentional. Please read carefully before adding, modifying, or auto-generating code.

---

## Coding Philosophy

This codebase follows the principles of:

- **KISS** – Keep it simple and self-explanatory.
- **DRY** – Don't repeat yourself. Reuse logic cleanly and clearly.
- **Clarity over cleverness** – Prioritize readability and long-term maintainability.
- **Explicit over implicit** – Avoid “magic.” Be direct.
- **Well-documented** – Every function, class, and service must be explained with meaningful docstrings.

---

## Guidelines

- Write clean, consistent Python 3.11+ code
- Follow PEP8 (with flexibility where readability matters)
- Use **type hints** consistently
- Use **docstrings** for:
  - All public functions and classes
  - Modules with meaningful logic
- Avoid global state and unnecessary complexity
- Never assume — every important behavior should be tested or documented
- Keep functions small and purpose-driven
- Group related logic in services (not bloated utils)

---

## Folder Structure (Initial Plan)

This structure will evolve, but this is the intended baseline.
app/
├── main.py # Entrypoint for FastAPI app
├── api/ # Route definitions (by domain)
│ ├── cards.py
│ └── collection.py
├── models/ # SQLAlchemy ORM models
│ ├── base.py
│ ├── card.py
│ └── collection.py
├── schemas/ # Pydantic request/response schemas
│ ├── card.py
│ └── collection.py
├── services/ # Business logic layer
│ ├── card_service.py
│ └── collection_service.py
├── db/ # Database connection and session management
│ ├── session.py
│ └── init_db.py
├── core/ # Internal helpers, constants, shared logic
│ └── config.py
├── tests/ # Test suite
│ ├── conftest.py
│ └── test_cards.py
└── init.py

---

## Development Rules

### Environment Consistency
- Local development must simulate the structure and behavior of the production environment as closely as possible.
- Docker is used to containerize and isolate services for local development, but **the codebase must not depend on Docker-specific paths or hacks**.
- All environment-specific settings must be abstracted via environment variables or configuration files (`.env` and `config.py`).
- Never hardcode credentials, ports, paths, or hostnames.
- Moving between `local`, `staging`, and `production` must not require structural code changes — only environment configuration changes.

### Security First
- All inputs must be validated using Pydantic schemas or typed interfaces.
- Never trust user input. Sanitize, validate, and restrict.
- Use proper password hashing (e.g., bcrypt or Argon2 via passlib if applicable).
- Use HTTPS in production and enforce secure CORS settings.
- Avoid exposing internal service logic or database structure via public endpoints.
- Secrets must never be committed. Use `.env`, Docker secrets, or mounted volumes for sensitive config.

### General Development Practices
- Use `async` endpoints and DB operations where supported.
- Always write testable code. If logic cannot be tested easily, restructure it.
- No placeholder logic unless clearly marked with `# TODO` or `raise NotImplementedError()`
- Keep functions short, named clearly, and scoped to a single purpose.
- Avoid circular imports and global state.
- Declare all dependencies in `requirements.txt` and pin versions when deploying.

### Service Metadata
- Every microservice must include a `version.json` file at the project root.
- This file contains service metadata such as version number, name, environment info, and release notes.
- It should be read by the application at runtime and made available (e.g., via a `/version` endpoint).
- This enables programmatic health checks, CI tagging, and easier debugging across environments.

---
## AI Agent-Specific Notes
If you're an AI agent writing or refactoring code:
- Don't guess structure. Refer to this file.
- If unsure, output the change as a *suggestion* or *commented block*.
- Avoid unnecessary abstraction (especially early).
- Every file or function you touch must include a short docstring that explains its purpose.

## Data Model ERD

The service maintains two core tables:

```
+-----------+      +--------------------+
|  cards    |1    *| collection_entries |
+-----------+      +--------------------+
| id (PK)   |<-----| card_id (FK)       |
| name      |      | user_id            |
| set       |      |  quantity          |  
| ...       |      | condition          |
+-----------+      | price_paid         |
                   | acquired_at        |
                   +--------------------+
```

`CollectionEntry.card_id` references `Card.id`, forming a one-to-many
relationship from cards to user-owned entries.
---
## Updates
This file will be updated continuously as the project evolves. Any structural changes or rules added here are binding across the entire `silph-cardvault` service.
For system-wide coordination across all microservices, refer to the `silph-docs` repository.
