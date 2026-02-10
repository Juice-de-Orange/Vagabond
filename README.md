# 🏔️ Vagabond

**Offline-first outdoor POI search engine for the Alps.**

> Find drinking water, shelters, supermarkets, toilets and more — even without
> internet. Upload a GPX track and get intelligent POI suggestions along your
> route, including walking time, reliability scores and opening hours.

⚠️ **Status: In active development (Phase 1 – Personal & Friends)**

---

## Features

- 🔍 **Radius-based POI search** with intelligent scoring
- 📂 **GPX analysis** — upload a track, get POIs along the route
- 📴 **Offline-first** — maps, POIs and routing work without internet
- 🌲 **Nature conservation** — warnings for protected areas
- ♿ **Accessibility** — wheelchair routing, TalkBack support
- 🔋 **Battery-optimized** — adaptive GPS strategy with 5 modes

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python 3.12+, FastAPI, PostgreSQL/PostGIS, Redis, GraphHopper |
| Android | Kotlin, Jetpack Compose, MapLibre, BRouter, Room |
| Infrastructure | Docker Compose, Cloudflare Tunnel, GitHub Actions |

## Self-Hosting

> Coming soon. Vagabond is designed to be self-hostable from day one.

## Development

> Coming soon. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

[AGPL v3](LICENSE) — Free to use, modify and self-host.
Modified hosted versions must share their changes.

**Map data:** © [OpenStreetMap](https://www.openstreetmap.org/copyright) contributors (ODbL)