from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.database import get_db

router = APIRouter()


@router.get("/api/v1/search")
async def search_pois(
    lat: float = Query(..., ge=-90, le=90, description="Breitengrad"),
    lon: float = Query(..., ge=-180, le=180, description="Längengrad"),
    radius: float = Query(1000, ge=100, le=50000, description="Suchradius in Metern"),
    poi_type: str | None = Query(None, description="POI-Kategorie filtern"),
    limit: int = Query(20, ge=1, le=50, description="Max Ergebnisse"),
    db: AsyncSession = Depends(get_db),
):
    """Sucht POIs im Umkreis einer Koordinate."""

    # Query dynamisch bauen statt NULL-Check in SQL
    where_type = "AND poi_type = :poi_type" if poi_type else ""

    query = text(f"""
        SELECT
            id, name, poi_type,
            ST_Y(geog::geometry) as lat,
            ST_X(geog::geometry) as lon,
            ST_Distance(geog, ST_MakePoint(:lon, :lat)::geography) as distance_m,
            reliability, opening_hours, wheelchair
        FROM pois
        WHERE ST_DWithin(geog, ST_MakePoint(:lon, :lat)::geography, :radius)
          {where_type}
        ORDER BY distance_m
        LIMIT :limit
    """)

    params = {"lat": lat, "lon": lon, "radius": radius, "limit": limit}
    if poi_type:
        params["poi_type"] = poi_type

    result = await db.execute(query, params)

    pois = [
        {
            "id": str(row.id),
            "name": row.name,
            "poi_type": row.poi_type,
            "lat": row.lat,
            "lon": row.lon,
            "distance_m": round(row.distance_m, 1),
            "reliability": row.reliability,
            "opening_hours": row.opening_hours,
            "wheelchair": row.wheelchair,
        }
        for row in result.fetchall()
    ]

    return {
        "count": len(pois),
        "center": {"lat": lat, "lon": lon},
        "radius_m": radius,
        "results": pois,
    }