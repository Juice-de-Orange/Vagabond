from sqlalchemy import Column, String, Float, Integer, DateTime, Boolean, BigInteger, text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import DeclarativeBase
from geoalchemy2 import Geography
from datetime import datetime, timezone


class Base(DeclarativeBase):
    pass


class POI(Base):
    __tablename__ = "pois"

    id = Column(UUID, primary_key=True, server_default=text("gen_random_uuid()"))
    osm_id = Column(BigInteger)
    osm_type = Column(String(10))
    name = Column(String)
    poi_type = Column(String(50), nullable=False)
    geog = Column(Geography("POINT", srid=4326), nullable=False)
    tags = Column(JSONB, server_default=text("'{}'"))
    opening_hours = Column(String)
    elevation_m = Column(Float)
    wheelchair = Column(String(20))
    last_osm_update = Column(DateTime(timezone=True))
    last_verified = Column(DateTime(timezone=True))
    verified_count = Column(Integer, default=0)
    reliability = Column(Float, default=0.5)
    is_seasonal = Column(Boolean, default=False)
    season_start = Column(Integer)
    season_end = Column(Integer)
    region = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=text("NOW()"))
    updated_at = Column(DateTime(timezone=True), server_default=text("NOW()"))