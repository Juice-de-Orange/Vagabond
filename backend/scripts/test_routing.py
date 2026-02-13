"""Schnelltest fuer GraphHopper-Anbindung."""

import asyncio
from app.core.routing import get_walking_time


async def main():
    # Mozartplatz -> Festung Hohensalzburg (kurz, steil)
    result = await get_walking_time(47.7984, 13.0478, 47.7952, 13.0475)
    if result:
        print("Mozartplatz -> Festung:")
        print(f"  Distanz:  {result['distance_m']}m")
        print(f"  Gehzeit:  {result['time_s']}s ({result['time_s'] // 60} min)")
        print(f"  Aufstieg: {result['ascend_m']}m")
        print(f"  Abstieg:  {result['descend_m']}m")
    else:
        print("Fehler: Keine Route berechnet")


if __name__ == "__main__":
    asyncio.run(main())