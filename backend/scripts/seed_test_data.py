"""Fügt Test-POIs rund um Salzburg ein."""

import asyncio
from sqlalchemy import text
from app.models.database import engine


TEST_POIS = [
    # Trinkwasser
    ("Trinkbrunnen Residenzplatz", "water", 47.7981, 13.0469, "Salzburg"),
    ("Brunnen Mirabellgarten", "water", 47.8052, 13.0425, "Salzburg"),
    ("Trinkwasser Kapuzinerberg", "water", 47.8029, 13.0556, "Salzburg"),
    # Supermärkte
    ("SPAR Getreidegasse", "supermarket", 47.7997, 13.0440, "Salzburg"),
    ("BILLA Linzer Gasse", "supermarket", 47.8028, 13.0456, "Salzburg"),
    ("Hofer Schallmoos", "supermarket", 47.8123, 13.0567, "Salzburg"),
    # Toiletten
    ("WC Mozartplatz", "toilet", 47.7984, 13.0484, "Salzburg"),
    ("WC Hauptbahnhof", "toilet", 47.8131, 13.0459, "Salzburg"),
    # Schutzhütten
    ("Stadtalm", "shelter", 47.7936, 13.0512, "Salzburg"),
    ("Untersberg Toni-Lenz-Hütte", "shelter", 47.7269, 13.0063, "Salzburg"),
    # Apotheken
    ("Apotheke Alter Markt", "pharmacy", 47.7987, 13.0467, "Salzburg"),
    # Restaurants
    ("Stiftskeller St. Peter", "restaurant", 47.7966, 13.0451, "Salzburg"),
    ("Augustiner Bräu", "restaurant", 47.8013, 13.0331, "Salzburg"),
    # Notfall
    ("Landeskrankenhaus Salzburg", "emergency", 47.7989, 13.0369, "Salzburg"),
]


async def seed():
    async with engine.begin() as conn:
        # Bestehende Testdaten löschen
        await conn.execute(text("DELETE FROM pois WHERE region = 'Salzburg'"))

        # Neue Testdaten einfügen
        for name, poi_type, lat, lon, region in TEST_POIS:
            await conn.execute(
                text("""
                    INSERT INTO pois (name, poi_type, geog, region, reliability)
                    VALUES (:name, :type, ST_MakePoint(:lon, :lat)::geography, :region, 0.8)
                """),
                {"name": name, "type": poi_type, "lat": lat, "lon": lon, "region": region},
            )

    print(f"✅ {len(TEST_POIS)} Test-POIs eingefügt")


if __name__ == "__main__":
    asyncio.run(seed())