from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.database import get_db
from app.core.routing import get_walking_time
from app.core.scoring import calculate_score, should_filter_closed

router = APIRouter()


@router.get("/api/v1/search")
async def search_pois(
    lat: float = Query(..., ge=-90, le=90, description="Breitengrad"),
    lon: float = Query(..., ge=-180, le=180, description="Laengengrad"),
    radius: float = Query(1000, ge=100, le=50000, description="Suchradius in Metern"),
    poi_type: str | None = Query(None, description="POI-Kategorie filtern"),
    limit: int = Query(20, ge=1, le=50, description="Max Ergebnisse"),
    accessible: bool = Query(False, description="Barrierefreiheits-Modus"),
    db: AsyncSession = Depends(get_db),
):
    """Sucht POIs im Umkreis einer Koordinate mit Scoring und Gehzeit."""

    where_type = "AND poi_type = :poi_type" if poi_type else ""

    # Mehr holen als limit, weil manche nach Filterung wegfallen
    fetch_limit = min(limit * 2, 50)

    query = text(f"""
        SELECT
            id, name, poi_type,
            ST_Y(geog::geometry) as lat,
            ST_X(geog::geometry) as lon,
            ST_Distance(geog, ST_MakePoint(:lon, :lat)::geography) as distance_m,
            reliability, opening_hours, wheelchair, verified_count
        FROM pois
        WHERE ST_DWithin(geog, ST_MakePoint(:lon, :lat)::geography, :radius)
          {where_type}
        ORDER BY distance_m
        LIMIT :fetch_limit
    """)

    params = {"lat": lat, "lon": lon, "radius": radius, "fetch_limit": fetch_limit}
    if poi_type:
        params["poi_type"] = poi_type

    result = await db.execute(query, params)
    rows = result.fetchall()

    pois = []
    for row in rows:
        # TODO: Oeffnungszeiten-Parser (Sprint 2)
        # is_open und opens_in_s kommen spaeter aus opening_hours.py
        is_open = None
        opens_in_s = None

        # Geschlossene POIs filtern
        if should_filter_closed(row.poi_type, is_open, opens_in_s=opens_in_s):
            continue

        # Gehzeit berechnen (nur fuer die naechsten 10)
        walking = None
        if len(pois) < 10:
            walking = await get_walking_time(lat, lon, row.lat, row.lon)

        score = calculate_score(
            distance_m=row.distance_m,
            max_distance_m=radius,
            poi_type=row.poi_type,
            time_s=walking["time_s"] if walking else None,
            reliability=row.reliability,
            verified_count=row.verified_count or 0,
            wheelchair=row.wheelchair,
            accessible_mode=accessible,
        )

        pois.append({
            "id": str(row.id),
            "name": row.name,
            "poi_type": row.poi_type,
            "lat": row.lat,
            "lon": row.lon,
            "distance_m": round(row.distance_m, 1),
            "walking_time_s": walking["time_s"] if walking else None,
            "walking_distance_m": walking["distance_m"] if walking else None,
            "ascend_m": walking["ascend_m"] if walking else None,
            "score": score,
            "reliability": row.reliability,
            "opening_hours": row.opening_hours,
            "wheelchair": row.wheelchair,
        })

    # Nach Score sortieren, auf limit beschraenken
    pois.sort(key=lambda p: p["score"], reverse=True)
    pois = pois[:limit]

    return {
        "count": len(pois),
        "center": {"lat": lat, "lon": lon},
        "radius_m": radius,
        "results": pois,
    }