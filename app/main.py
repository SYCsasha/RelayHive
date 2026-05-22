"""Main FastAPI application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.api.routes import health, work_orders, ai_agents

settings = get_settings()

app = FastAPI(
    title="RelayHive - AI Work Order System",
    description="AI-native work order system with relay chain capabilities",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(health.router, tags=["health"])
app.include_router(
    ai_agents.router,
    prefix=settings.API_V1_PREFIX,
    tags=["ai_agents"]
)
app.include_router(
    work_orders.router,
    prefix=settings.API_V1_PREFIX,
    tags=["work_orders"]
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
