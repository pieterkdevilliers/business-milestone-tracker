from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.tracker import router as tracker_router
from app.db.base import Base
from app.db.seed import seed_if_empty
from app.db.session import AsyncSessionLocal, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSessionLocal() as session:
        await seed_if_empty(session)
    yield


app = FastAPI(title="Milestone Tracker API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tracker_router)


@app.get("/")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
