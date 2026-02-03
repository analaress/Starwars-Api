from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.routes import films, people, auth, stats
from app.clients import swapi_client
from app.db.base import Base
from app.db.session import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(
    title="Star Wars API",
    description="API baseada na SWAPI",
    version="1.0.0",
    lifespan=lifespan
)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(people.router)
app.include_router(films.router)
app.include_router(stats.router)

@app.get("/")
async def health_check():
    return {"status": "ok"}
