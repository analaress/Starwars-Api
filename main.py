from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.routes import films, people, auth, stats
from vellox import Vellox
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(
    title="Star Wars API",
    description="API baseada na SWAPI",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    openapi_url="/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(people.router)
app.include_router(films.router)
app.include_router(stats.router)

@app.get("/")
async def health_check():
    return {"status": "ok"}

vellox = Vellox(app=app, lifespan="off")

def handler(request):
    return vellox(request)