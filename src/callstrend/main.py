from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from callstrend.api.routes.health import router as health_router
from callstrend.api.routes.tickets import router as tickets_router

_DESCRIPTION = """
## CallsTrend API — POC de Help Desk com Triagem Automática

Esta API é o núcleo do sistema CallsTrend.  
Ela expõe os recursos necessários para **abertura, triagem automática e gestão de chamados técnicos**.

### Fluxo principal

1. O usuário abre um chamado com título e descrição livres (`POST /api/v1/tickets`).
2. O sistema classifica automaticamente o chamado por **categoria** e **prioridade** usando um módulo de IA heurístico.
3. O chamado fica disponível para consulta com a classificação sugerida (`GET /api/v1/tickets`).
4. O administrador pode revisar e corrigir categoria, prioridade e status (`PATCH /api/v1/tickets/{ticket_id}`).

### Enums disponíveis

| Enum | Valores possíveis |
|---|---|
| **Categoria** | `Hardware`, `Software`, `Rede`, `Acesso`, `Outros` |
| **Prioridade** | `Baixa`, `Media`, `Alta` |
| **Status** | `EmTriagem`, `Aberto`, `EmAtendimento`, `Resolvido`, `Fechado` |

### Módulo de triagem automática

O classificador atual usa um algoritmo baseado em palavras-chave.  
As ocorrências no **título** têm peso 2; as ocorrências na **descrição** têm peso 1.  
Cada chamado recebe um campo `classification_confidence` (0.0–1.0) e `classification_rationale`  
para transparência sobre a decisão automática.
"""

app = FastAPI(
    title="CallsTrend API",
    version="0.1.0",
    summary="POC de Help Desk com triagem automática de chamados por IA.",
    description=_DESCRIPTION,
    contact={
        "name": "CallsTrend — Projeto Acadêmico",
        "url": "https://github.com/GustavoLazoti/CallsTrend",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=[
        {
            "name": "root",
            "description": "Rota raiz da API.",
        },
        {
            "name": "health",
            "description": "Verificação de disponibilidade da aplicação.",
        },
        {
            "name": "tickets",
            "description": (
                "Gerenciamento de chamados técnicos.  \n"
                "Permite abrir, listar e atualizar chamados com triagem automática por IA."
            ),
        },
    ],
)

app.include_router(health_router)
app.include_router(tickets_router)


@app.get(
    "/",
    tags=["root"],
    summary="Rota raiz",
    description="Retorna uma mensagem de boas-vindas e o link para a documentação interativa.",
    response_description="Mensagem de status e URL da documentação.",
)
def root() -> dict[str, str]:
    return {
        "message": "CallsTrend POC em execução.",
        "docs": "/docs",
    }
