# SILPH-cardvault

**silph-cardvault** is one of the core microservices in **Project SILPH**, a modular, microservice-based Pokémon TCG platform purpose-built for collectors in the Philippines.
This service is responsible for managing all Pokémon card data and user-owned collections. It provides the foundation for catalogue, trade, and search features across the platform.

---

## Purpose and Role

This service has two key responsibilities:

1. **Global Cards Database**  
   Hosts a complete reference of all Pokémon cards, pulled and normalized from the [PokéTCG.io API](https://pokemontcg.io). This dataset is the single source of truth for card metadata used across other services (e.g., marketplace listings, OCR matching).

2. **User Collections**  
   Manages individual user collections, allowing them to catalogue the cards they personally own. This includes tracking quantity, condition, pricing notes, and other metadata tied to specific users.
   
No additional features are implemented or planned at this time. Any new responsibilities will be defined separately and evaluated based on project-wide architecture.

---

## Tech Stack

This service is backend-only.

- **Language:** Python 3.11+
- **Framework:** FastAPI
- **Database:** PostgreSQL
- **Containerization:** Docker / Docker Compose
- **ORM:** SQLAlchemy (async)
- **Documentation:** Auto-generated via OpenAPI (`/docs`)

---

## Usage

### Cloning the Repository

```bash
git clone https://github.com/YOUR_USERNAME/silph-cardvault.git
cd silph-cardvault
