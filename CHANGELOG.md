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

## [0.1.3] – 2025-06-25
### Added
- Async-compatible `BaseModel` shared across models
- Alembic migration setup

## [0.1.4] – 2025-06-25
### Added
- `/health` endpoint for basic service checks with auto-generated OpenAPI docs
---

## [0.1.6] – 2025-06-25
### Added
- Full card sync loop using ID-based diffing from PokéTCG.io
- `fetch_all_remote_card_ids()` to pull all card IDs via paginated API
- `get_all_local_card_ids(session)` to retrieve existing card IDs from local DB
- `sync_missing_cards(session)` to compute missing IDs and import them safely
- Updated `import_card()` flow: fetch → normalize → store
- Safe `store_card()` logic using SQLAlchemy upsert pattern
- All sync logic contained within `GlobalCardService` class
- Protected against PokéTCG pagination reordering issues by avoiding page-based state

### Changed
- Switched from page-based sync idea to safer ID-diff model for resilience and correctness

### Notes
- Sync logic is production-safe and can be wired into CLI or admin-only endpoints.
- Rate-limiting, logging, or batch throttling may be added in future minor releases.

## [Unreleased]
### Planned
- Build Functions to support endpoints for this microservices
Global Card Reference
  - Fetch Card Data  - Get raw data for a specific card from PokeTCG.io
  - Normalize Card Data - Convert PokeTCG data to match your DB Model
  - Store Card - Insert/Update a card record in your DB
  - Get all card ID available in PokeTCG.io
  - Get all card ID available in DB
  - Get missing cards from DB
  - Bulk Fetch Cards IDs- Get all raw data for all specific card ids missing in DB from POkeTCG.io
  - Sync Card Batch - Batch import multiple card (fetch, normalize, store to DB)
  - search card - return filtered cards
  - get all sets

USer Collection Logic
  - Add card to collection
  - Update Collection entry
  - Remove card from collection
  - get user collection
  - get card with user info
  - bulk add collection

Utility
  - Get service Version
  - Validate Card Id
  - Check CArd Exists Locally

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

