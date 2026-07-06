from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.challenges import router as challenges_router


app = FastAPI(
    title="Intelligent Cognitive Alarm Platform",
    version="1.0.0",
    description="Cognitive Challenge Bank module API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(challenges_router)


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    """Return a lightweight health status."""

    return {"status": "ok"}
