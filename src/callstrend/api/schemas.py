from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from callstrend.domain.enums import Category, Priority, TicketStatus
from callstrend.domain.models import Ticket


class CreateTicketRequest(BaseModel):
    """Payload para abertura de um novo chamado técnico."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "title": "VPN sem conectar",
                    "description": "Não consigo acessar o sistema interno pela VPN desde a manhã.",
                    "requester_name": "Maria Silva",
                    "requester_email": "maria@empresa.com",
                }
            ]
        }
    )

    title: str = Field(
        min_length=3,
        max_length=120,
        description="Título curto e objetivo do problema técnico. Mínimo 3, máximo 120 caracteres.",
        examples=["VPN sem conectar", "Impressora não imprime"],
    )
    description: str = Field(
        min_length=10,
        max_length=2000,
        description=(
            "Descrição detalhada do problema. "
            "Quanto mais detalhado, mais precisa será a classificação automática. "
            "Mínimo 10, máximo 2000 caracteres."
        ),
        examples=["Não consigo acessar o sistema interno pela VPN desde a manhã."],
    )
    requester_name: str = Field(
        min_length=3,
        max_length=80,
        description="Nome completo de quem está abrindo o chamado.",
        examples=["Maria Silva"],
    )
    requester_email: str = Field(
        min_length=5,
        max_length=160,
        description="E-mail de contato do solicitante.",
        examples=["maria@empresa.com"],
    )


class UpdateTicketRequest(BaseModel):
    """Payload para atualização administrativa de um chamado.
    Todos os campos são opcionais — apenas os campos enviados serão alterados.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "status": "EmAtendimento",
                    "priority": "Alta",
                },
                {
                    "category": "Rede",
                },
                {
                    "status": "Resolvido",
                },
            ]
        }
    )

    status: TicketStatus | None = Field(
        default=None,
        description=(
            "Novo status do chamado. "
            "Valores aceitos: `EmTriagem`, `Aberto`, `EmAtendimento`, `Resolvido`, `Fechado`."
        ),
        examples=["EmAtendimento"],
    )
    category: Category | None = Field(
        default=None,
        description=(
            "Correção manual da categoria sugerida pela IA. "
            "Valores aceitos: `Hardware`, `Software`, `Rede`, `Acesso`, `Outros`."
        ),
        examples=["Rede"],
    )
    priority: Priority | None = Field(
        default=None,
        description=(
            "Correção manual da prioridade sugerida pela IA. "
            "Valores aceitos: `Baixa`, `Media`, `Alta`."
        ),
        examples=["Alta"],
    )


class TicketResponse(BaseModel):
    """Representação completa de um chamado, incluindo a classificação automática da IA."""

    model_config = ConfigDict(
        use_enum_values=True,
        json_schema_extra={
            "examples": [
                {
                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "title": "VPN sem conectar",
                    "description": "Não consigo acessar o sistema interno pela VPN desde a manhã.",
                    "requester_name": "Maria Silva",
                    "requester_email": "maria@empresa.com",
                    "created_at": "2026-05-12T21:00:00Z",
                    "status": "Aberto",
                    "category": "Rede",
                    "priority": "Alta",
                    "classification_confidence": 0.83,
                    "classification_rationale": (
                        "Categoria sugerida: Rede (score 2). "
                        "Prioridade sugerida: Alta (score 2)."
                    ),
                }
            ]
        },
    )

    id: str = Field(description="Identificador único do chamado (UUID v4).")
    title: str = Field(description="Título do chamado informado pelo solicitante.")
    description: str = Field(description="Descrição detalhada do problema.")
    requester_name: str = Field(description="Nome do solicitante.")
    requester_email: str = Field(description="E-mail do solicitante.")
    created_at: datetime = Field(description="Data e hora de abertura do chamado (UTC).")
    status: str = Field(
        description=(
            "Status atual do chamado. "
            "Possíveis valores: `EmTriagem`, `Aberto`, `EmAtendimento`, `Resolvido`, `Fechado`."
        )
    )
    category: str = Field(
        description=(
            "Categoria atribuída ao chamado (automática ou corrigida pelo administrador). "
            "Possíveis valores: `Hardware`, `Software`, `Rede`, `Acesso`, `Outros`."
        )
    )
    priority: str = Field(
        description=(
            "Prioridade atribuída ao chamado (automática ou corrigida pelo administrador). "
            "Possíveis valores: `Baixa`, `Media`, `Alta`."
        )
    )
    classification_confidence: float = Field(
        description=(
            "Nível de confiança da classificação automática, de 0.0 a 1.0. "
            "Valores mais altos indicam maior certeza do módulo de IA."
        )
    )
    classification_rationale: str = Field(
        description=(
            "Justificativa textual da classificação automática. "
            "Explica quais sinais foram encontrados no texto para inferir categoria e prioridade."
        )
    )

    @classmethod
    def from_ticket(cls, ticket: Ticket) -> "TicketResponse":
        return cls(
            id=ticket.id,
            title=ticket.title,
            description=ticket.description,
            requester_name=ticket.requester_name,
            requester_email=ticket.requester_email,
            created_at=ticket.created_at,
            status=ticket.status.value,
            category=ticket.category.value,
            priority=ticket.priority.value,
            classification_confidence=ticket.classification_confidence,
            classification_rationale=ticket.classification_rationale,
        )
