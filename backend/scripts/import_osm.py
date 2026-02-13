"""Importiert POIs aus einer OSM PBF-Datei in die PostGIS-Datenbank."""

import asyncio
import time

import osmium
from sqlalchemy import text

from app.models.database import engine

# OSM-Tag-Mapping: Welche Tags wollen wir als welche POI-Kategorie?
POI_TAGS = {
    "water": [
        {"amenity": "drinking_water"},
        {"man_made": "water_well"},
    ],
    "supermarket": [
        {"shop": "supermarket"},
        {"shop": "convenience"},
        {"shop": "general"},
    ],
    "toilet": [
        {"amenity": "toilets"},
    ],
    "shelter": [
        {"amenity": "shelter"},
        {"tourism": "alpine_hut"},
        {"tourism": "wilderness_hut"},
    ],
    "pharmacy": [
        {"amenity": "pharmacy"},
    ],
    "emergency": [
        {"amenity": "hospital"},
    ],
    "restaurant": [
        {"amenity": "restaurant"},
        {"amenity": "cafe"},
        {"amenity": "biergarten"},
    ],
    "parking": [
        {"amenity": "parking"},
        {"highway": "trailhead"},
    ],
    "waste": [
        {"amenity": "waste_basket"},
        {"amenity": "waste_disposal"},
    ],
}


def match_poi_type(tags) -> str | None:
    """Prüft ob die OSM-Tags zu einer unserer POI-Kategorien passen."""
    for poi_type, tag_list in POI_TAGS.items():
        for tag_match in tag_list:
            if all(tags.get(k) == v for k, v in tag_match.items()):
                return poi_type
    return None


class POIHandler(osmium.SimpleHandler):
    """Liest OSM-Nodes und sammelt passende POIs."""

    def __init__(self):
        super().__init__()
        self.pois = []
        self.count = 0

    def node(self, n):
        self.count += 1
        if self.count % 5_000_000 == 0:
            print(f"  ... {self.count:,} Nodes verarbeitet, {len(self.pois)} POIs gefunden")

        tags = {t.k: t.v for t in n.tags}
        poi_type = match_poi_type(tags)

        if poi_type and n.location.valid():
            self.pois.append({
                "osm_id": n.id,
                "name": tags.get("name"),
                "poi_type": poi_type,
                "lat": n.location.lat,
                "lon": n.location.lon,
                "opening_hours": tags.get("opening_hours"),
                "wheelchair": tags.get("wheelchair"),
                "tags": tags,
            })


async def import_to_db(pois: list[dict]):
    """Fügt die gesammelten POIs in die Datenbank ein."""
    async with engine.begin() as conn:
        # Alte OSM-Daten löschen
        await conn.execute(text("DELETE FROM pois WHERE osm_id IS NOT NULL"))

        # Batch-Insert in Gruppen von 500
        batch_size = 500
        for i in range(0, len(pois), batch_size):
            batch = pois[i : i + batch_size]
            for poi in batch:
                await conn.execute(
                    text("""
                        INSERT INTO pois (osm_id, osm_type, name, poi_type, geog,
                                         opening_hours, wheelchair, region)
                        VALUES (:osm_id, 'node', :name, :poi_type,
                                ST_MakePoint(:lon, :lat)::geography,
                                :opening_hours, :wheelchair, 'alps')
                    """),
                    poi,
                )
            print(f"  ... {min(i + batch_size, len(pois))}/{len(pois)} in DB geschrieben")


async def main():
    pbf_path = "../data/alps-latest.osm.pbf"

    print("🔍 Lese OSM-Datei...")
    start = time.time()

    handler = POIHandler()
    handler.apply_file(pbf_path, locations=False)

    read_time = time.time() - start
    print(f"✅ {len(handler.pois):,} POIs in {read_time:.1f}s gefunden")

    print("💾 Schreibe in Datenbank...")
    start = time.time()

    await import_to_db(handler.pois)

    write_time = time.time() - start
    print(f"✅ Import abgeschlossen in {write_time:.1f}s")


if __name__ == "__main__":
    asyncio.run(main())