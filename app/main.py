from fastapi import FastAPI
from app.api.routes import people
from app.clients import swapi_client

app = FastAPI(
    title="Star Wars API",
    description="API baseada na SWAPI",
    version="1.0.0"
)

app.include_router(people.router)

@app.on_event("shutdown")
async def shutdown_event():
    await swapi_client.client.aclose()

@app.get("/")
def health_check():
    return {"status": "ok"}
