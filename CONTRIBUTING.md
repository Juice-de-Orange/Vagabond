# Contributing to Vagabond

Thank you for your interest in contributing! 🏔️

## Getting Started

### Prerequisites

- Docker & Docker Compose v2
- Git
- Python 3.12+ (for backend development)
- Android Studio (for app development)

### Development Setup
```bash
# Clone the repository
git clone https://github.com/Juice-de-Orange/vagabond.git
cd vagabond

# Copy environment variables
cp .env.example .env
# Edit .env with your values

# Start backend services
docker compose up -d

# Run backend tests
docker compose exec api pytest
```

## Workflow

1. **Fork** the repository
2. **Create a branch** from `main`: `git checkout -b feat/my-feature`
3. **Make your changes** with clear, focused commits
4. **Push** to your fork: `git push origin feat/my-feature`
5. **Open a Pull Request** against `main`

## Commit Messages

We use [Conventional Commits](https://www.conventionalcommits.org/):
```
feat(search): add category filter to radius search
fix(gpx): handle tracks with missing elevation data
docs: update self-hosting guide
chore(docker): upgrade PostGIS to 17-3.5
```

## Code Standards

### Python (Backend)
- Formatter: `ruff format`
- Linter: `ruff check`
- Type hints on all functions
- Docstrings on public functions

### Kotlin (Android)
- Follow [Kotlin coding conventions](https://kotlinlang.org/docs/coding-conventions.html)
- Jetpack Compose best practices

## What to Contribute

Check out our [issues labeled "good first issue"](https://github.com/Juice-de-Orange/vagabond/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) for beginner-friendly tasks.

Areas where we especially need help:
- OSM tag mappings for POI categories
- Translations (German, Italian, French, Slovenian)
- Accessibility testing
- Documentation

## Code of Conduct

Please read our [Code of Conduct](CODE_OF_CONDUCT.md). We are committed to
providing a welcoming and inclusive experience for everyone.