from fastapi import FastAPI

from callstrend.api.routes.health import router as health_router
from callstrend.api.routes.tickets import router as tickets_router


app = FastAPI(
    title="CallsTrend API",
    version="0.1.0",
    description="POC de Help Desk com triagem automática demonstrativa.",
)

app.include_router(health_router)
app.include_router(tickets_router)


@app.get("/", tags=["root"])
def root() -> dict[str, str]:
    return {
        "message": "CallsTrend POC em execução.",
        "docs": "/docs",
    }
