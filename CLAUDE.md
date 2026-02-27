# CLAUDE.md — Vagabond

This file provides guidance for AI assistants (Claude and others) working in this repository.

---

## Project Overview

**Vagabond** is an offline-first outdoor POI (Point of Interest) search engine for the Alps. It lets users find drinking water, shelters, supermarkets, toilets, and other resources — even without internet access. Users can upload a GPX track and receive intelligent POI suggestions along the route, including walking time, reliability scores, and opening hours.

**Current status:** Phase 1 — Personal & Friends. The repository contains infrastructure configuration and documentation; backend and Android source code are not yet committed (placeholder directories only).

**License:** AGPL v3 — modifications to hosted versions must be shared publicly.

---

## Repository Structure

```
Vagabond/
├── android/                # Android app (Kotlin/Jetpack Compose) — placeholder
├── backend/                # FastAPI backend (Python 3.12+) — placeholder
├── shared/                 # Shared code/resources — placeholder
├── docs/                   # Documentation — placeholder
├── config/
│   └── graphhopper.yml     # GraphHopper routing engine configuration
├── .env.example            # Environment variable template
├── docker-compose.yml      # Container orchestration (db, redis, graphhopper)
├── CHANGELOG.md            # Version history (Conventional Changelog format)
├── CONTRIBUTING.md         # Developer setup and workflow
├── SECURITY.md             # Vulnerability reporting and security policy
├── CODE_OF_CONDUCT.md      # Contributor Covenant 2.1
└── LICENSE                 # AGPL v3
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.12+, FastAPI, PostgreSQL 17 + PostGIS 3.5, Redis 8 |
| Routing | GraphHopper (israelhikingmap image), SRTM elevation, OSM data |
| Android | Kotlin, Jetpack Compose, MapLibre, BRouter, Room |
| Infrastructure | Docker Compose, Cloudflare Tunnel, GitHub Actions (planned) |
| Maps | OpenStreetMap data (ODbL) |

---

## Development Setup

### Prerequisites

- Docker & Docker Compose v2
- Git
- Python 3.12+ (for backend work)
- Android Studio (for Android work)

### First-time setup

```bash
git clone https://github.com/Juice-de-Orange/vagabond.git
cd vagabond
cp .env.example .env
# Fill in .env values (see Environment Variables below)
docker compose up -d
```

### Running backend tests

```bash
docker compose exec api pytest
```

### Stopping services

```bash
docker compose down
```

---

## Environment Variables

Copy `.env.example` to `.env` and fill in the values. Never commit `.env`.

| Variable | Description | Example |
|---|---|---|
| `DB_PASSWORD` | PostgreSQL password | `openssl rand -hex 32` |
| `POSTGRES_DB` | Database name | `vagabond` |
| `POSTGRES_USER` | Database user | `vagabond` |
| `REDIS_URL` | Redis connection string | `redis://redis:6379/0` |
| `API_KEY` | API authentication key | `openssl rand -hex 32` |
| `AUTH_MODE` | Auth strategy: `apikey` (Phase 1) or `jwt` (Phase 2) | `apikey` |
| `GRAPHHOPPER_URL` | Internal GraphHopper endpoint | `http://graphhopper:8989` |

---

## Infrastructure Services (Docker Compose)

### PostgreSQL with PostGIS (`db`)
- Image: `postgis/postgis:17-3.5`
- Memory limit: 1 GB
- Health check: `pg_isready`
- Persistent data: `pgdata` volume

### Redis (`redis`)
- Image: `redis:8-alpine`
- Memory limit: 300 MB, eviction policy: `allkeys-lru`
- Health check: `redis-cli ping`
- Persistent data: `redisdata` volume

### GraphHopper (`graphhopper`)
- Image: `israelhikingmap/graphhopper:latest`
- JVM heap: `-Xmx8g -Xms2g` (requires ~9 GB RAM)
- OSM input: `./data/alps-latest.osm.pbf` (must be downloaded manually)
- Routing profile: `hike` (ignores motorways and trunks)
- Elevation: SRTM provider
- Startup time: up to 600 seconds on first run (elevation cache build)
- Health check: `GET http://localhost:8989/health`
- Persistent data: `ghdata` volume
- Config: `./config/graphhopper.yml`

**Note:** The `./data/alps-latest.osm.pbf` file is not in the repository. Download it from Geofabrik before starting GraphHopper.

---

## Code Conventions

### Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat(search): add category filter to radius search
fix(gpx): handle tracks with missing elevation data
docs: update self-hosting guide
chore(docker): upgrade PostGIS to 17-3.5
```

Types: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`, `ci`

### Python (Backend)

- Formatter: `ruff format`
- Linter: `ruff check`
- Type hints required on all functions
- Docstrings required on public functions
- No secrets in code — use environment variables

### Kotlin (Android)

- Follow [Kotlin coding conventions](https://kotlinlang.org/docs/coding-conventions.html)
- Jetpack Compose best practices
- Offline-first: all core features must work without network

### Branch Naming

- Feature branches: `feat/<short-description>`
- Bug fixes: `fix/<short-description>`
- Docs: `docs/<short-description>`

---

## Security Constraints

These are hard rules — do not violate them:

- **GPS coordinates are never logged server-side** (privacy-critical)
- All API communication uses HTTPS only
- Secrets managed via environment variables, never hardcoded
- Docker containers run as non-root with minimal capabilities
- Never commit `.env` or any file containing secrets
- Report vulnerabilities privately (see `SECURITY.md`), not via public issues

---

## Key Design Principles

1. **Offline-first** — maps, POIs, and routing must work without internet
2. **Privacy-focused** — no server-side GPS logging
3. **Hiking-specific** — routing ignores motorways/trunks; uses SRTM elevation
4. **Battery-optimized** — Android GPS manager supports 5 adaptive modes
5. **Accessible** — TalkBack support, wheelchair routing planned
6. **Self-hostable** — designed to be deployed independently from day one

---

## Planned Features (Not Yet Implemented)

- FastAPI backend with PostGIS geospatial queries and Redis caching
- POI scoring algorithm (reliability, walking time, opening hours)
- GPX track upload and analysis
- Android app with MapLibre maps and BRouter offline routing
- GitHub Actions CI/CD with Trivy dependency scanning
- Translations: German, Italian, French, Slovenian
- Nature conservation area warnings
- JWT authentication (Phase 2)
- Self-hosting documentation

---

## Contribution Areas

From `CONTRIBUTING.md`, help is especially needed in:

- OSM tag mappings for POI categories
- Translations (German, Italian, French, Slovenian)
- Accessibility testing
- Documentation

See [good first issues](https://github.com/Juice-de-Orange/vagabond/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).
