"""FastAPI application entry for RelayHive skeleton."""

from fastapi import FastAPI

app = FastAPI(
    title="RelayHive",
    version="0.1.0",
    description="Distributed AI Task Operating System skeleton",
)


@app.get("/", tags=["system"])
def root() -> dict[str, str]:
    """Lightweight root endpoint for startup verification."""
    return {"service": "RelayHive", "status": "running"}


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    """Health check endpoint for local/CI probes."""
    return {"status": "ok"}
