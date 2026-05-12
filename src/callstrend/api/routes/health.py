from fastapi import APIRouter


router = APIRouter(tags=["health"])


@router.get(
    "/health",
    summary="Health check",
    description=(
        "Verifica se a aplicação está no ar e pronta para receber requisições.  \n"
        "Não depende de nenhum recurso externo (banco de dados, IA, etc.)."
    ),
    response_description="Objeto JSON com o campo `status: ok` quando a API está disponível.",
    responses={
        200: {
            "description": "API disponível.",
            "content": {"application/json": {"example": {"status": "ok"}}},
        }
    },
)
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
