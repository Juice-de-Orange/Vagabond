"""GraphHopper Client fuer Gehzeit-Berechnung."""

import httpx
from app.config import settings


async def get_walking_time(
    from_lat: float,
    from_lon: float,
    to_lat: float,
    to_lon: float,
) -> dict | None:
    """Berechnet Gehzeit und Distanz zwischen zwei Punkten via GraphHopper.

    Returns:
        dict mit distance_m, time_s, ascend_m, descend_m
        oder None bei Fehler (z.B. kein Weg gefunden)
    """
    url = (
        f"{settings.graphhopper_url}/route"
        f"?point={from_lat},{from_lon}"
        f"&point={to_lat},{to_lon}"
        f"&profile=hike"
        f"&calc_points=true"
        f"&instructions=false"
        f"&elevation=true"
    )

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()

            path = data["paths"][0]
            return {
                "distance_m": round(path["distance"], 1),
                "time_s": round(path["time"] / 1000),
                "ascend_m": round(path.get("ascend", 0), 1),
                "descend_m": round(path.get("descend", 0), 1),
            }
    except Exception as e:
        print(f"Routing-Fehler: {e}")
        return None