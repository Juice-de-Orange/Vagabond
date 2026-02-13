from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.database import engine, get_db
from app.models.poi import Base
from app.api.routes.search import router as search_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database tables created")
    yield
    await engine.dispose()


app = FastAPI(
    title="Vagabond API",
    description="Offline-First Outdoor POI Search Engine",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(search_router)


@app.get("/api/v1/health")
async def health(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT PostGIS_Version()"))
    postgis_version = result.scalar()
    return {
        "status": "ok",
        "postgis": postgis_version,
    }