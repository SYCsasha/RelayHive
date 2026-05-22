"""RelayHive backend entrypoint.

MVP scope:
- FastAPI app bootstrap
- Task Center create/list APIs
- Tag Protocol v1 data structures
"""

from fastapi import FastAPI

from app.api.tasks import router as task_router

app = FastAPI(
    title="RelayHive Backend",
    version="0.1.0",
    description="Distributed AI task relay operating backend.",
)
app.include_router(task_router)


@app.get("/healthz", tags=["system"])
def healthz() -> dict[str, str]:
    return {"status": "ok"}
