# CHANGELOG – silph-cardvault

All notable changes to this service will be documented in this file.

This project uses [Semantic Versioning](https://semver.org/) (MAJOR.MINOR.PATCH), and each change is tracked clearly for both internal review and external collaboration.

---

## [0.1.0] – 2025-06-24
### Added
- Initial scaffold for silph-cardvault microservice
- Project structure defined (see `AGENT.md`)
- `README.md`, `AGENT.md`, and `version.json` created
- Documentation for purpose, boundaries, and usage
- Confirmed service responsibilities:
  - Global card reference DB
  - User-owned card catalogue

### Notes
- No API or models implemented yet — this is the documentation baseline for the service

---

## [0.1.1] – 2025-06-24
### Added
- Initial database schema with `Card` model representing global Pokémon cards

---

## [0.1.2] – 2025-06-25
### Added
- `CollectionEntry` model for tracking user-owned cards

---

## [Unreleased]
### Planned

- Build modular, async-compatible SQLAlchemy models with a shared `BaseModel`
- Normalize and store card data pulled from the PokéTCG.io API
- Create a sync pipeline that pulls cards from the API in batches and updates/inserts records safely
- Add internal logging and basic rate-limit protection to the sync tool
- Design a flexible method for syncing by set, by ID list, or full refresh
- Seed card data manually for testing via CLI or seed script
- Create Pydantic schemas for cards and user collection entries
- Expose public `/cards` endpoints with filtering, search, and pagination
- Expose `GET /cards/{id}` for full card metadata lookup
- Expose `/my-catalogue` endpoints for user-specific collection management (GET, POST, PATCH, DELETE)
- Define standard response schema with consistent envelope structure
- Simulate or integrate user ID context while auth layer is still in development
- Expose `/version` endpoint that reads from `version.json` at runtime
- Organize route logic into clearly defined routers (`cards`, `collection`)
- Implement lightweight dependency injection for DB session and settings
- Build test suite structure (e.g., using Pytest + TestClient)
- Define response contract for “merged” card + collection views (e.g., card metadata with user-specific condition/quantity)
- Tag or flag local-specific metadata for future pricing tools (e.g., PH-local price tiers or store tags)
- Keep schema migration tooling (e.g., Alembic) ready but not overused
- Design the folder layout and service structure to scale with future use cases (like visual card matcher, deduper, or user tagging)
- Document everything with docstrings — every model, route, and service must describe its role
- Ensure Docker-based dev environment mirrors production assumptions cleanly
- Make `version.json` modifiable without needing a code change (decouple metadata from logic)
- Provide clean example `.env` and optionally `.env.test` for local dev consistency
- Future-proof everything for data sync safety (e.g., hash checks or delta logic if needed)

