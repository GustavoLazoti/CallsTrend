from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from callstrend.api.dependencies import (
    get_create_ticket_use_case,
    get_list_tickets_use_case,
    get_update_ticket_use_case,
)
from callstrend.api.schemas import CreateTicketRequest, TicketResponse, UpdateTicketRequest
from callstrend.application.dto import CreateTicketCommand, UpdateTicketCommand
from callstrend.application.exceptions import TicketNotFoundError
from callstrend.application.use_cases import (
    CreateTicketUseCase,
    ListTicketsUseCase,
    UpdateTicketUseCase,
)


router = APIRouter(prefix="/api/v1/tickets", tags=["tickets"])


@router.post(
    "",
    response_model=TicketResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Abrir chamado",
    description=(
        "Registra um novo chamado técnico e executa a triagem automática via IA.  \n\n"
        "**Fluxo interno:**\n"
        "1. O chamado é criado com status `EmTriagem`.\n"
        "2. O módulo de IA analisa título e descrição e sugere uma **categoria** e **prioridade**.\n"
        "3. O chamado é atualizado para status `Aberto` com a classificação aplicada.\n"
        "4. A resposta retorna o chamado já classificado, com `classification_confidence` e `classification_rationale`."
    ),
    response_description="Chamado criado e classificado automaticamente.",
    responses={
        201: {"description": "Chamado criado com sucesso."},
        422: {"description": "Dados de entrada inválidos (validação Pydantic)."},
    },
)
def create_ticket(
    request: CreateTicketRequest,
    use_case: Annotated[CreateTicketUseCase, Depends(get_create_ticket_use_case)],
) -> TicketResponse:
    ticket = use_case.execute(
        CreateTicketCommand(
            title=request.title,
            description=request.description,
            requester_name=request.requester_name,
            requester_email=request.requester_email,
        )
    )
    return TicketResponse.from_ticket(ticket)


@router.get(
    "",
    response_model=list[TicketResponse],
    summary="Listar chamados",
    description=(
        "Retorna todos os chamados registrados, em ordem de criação.  \n\n"
        "Cada item inclui a classificação automática aplicada pela IA e o status atual."
    ),
    response_description="Lista de todos os chamados.",
    responses={
        200: {"description": "Lista de chamados retornada com sucesso."},
    },
)
def list_tickets(
    use_case: Annotated[ListTicketsUseCase, Depends(get_list_tickets_use_case)],
) -> list[TicketResponse]:
    return [TicketResponse.from_ticket(ticket) for ticket in use_case.execute()]


@router.patch(
    "/{ticket_id}",
    response_model=TicketResponse,
    summary="Atualizar chamado (gestão administrativa)",
    description=(
        "Permite que o administrador revise e corrija os dados de um chamado.  \n\n"
        "Todos os campos do body são **opcionais** — apenas os campos enviados serão alterados.  \n\n"
        "**Casos de uso típicos:**\n"
        "- Corrigir categoria ou prioridade sugerida incorretamente pela IA.\n"
        "- Avançar o status do chamado (`EmAtendimento`, `Resolvido`, `Fechado`).\n"
        "- Combinar atualização de status e classificação em uma única chamada."
    ),
    response_description="Chamado atualizado com os dados enviados.",
    responses={
        200: {"description": "Chamado atualizado com sucesso."},
        404: {"description": "Chamado não encontrado para o `ticket_id` informado."},
        422: {"description": "Dados de entrada inválidos (validação Pydantic)."},
    },
)
def update_ticket(
    ticket_id: str,
    request: UpdateTicketRequest,
    use_case: Annotated[UpdateTicketUseCase, Depends(get_update_ticket_use_case)],
) -> TicketResponse:
    try:
        ticket = use_case.execute(
            UpdateTicketCommand(
                ticket_id=ticket_id,
                status=request.status,
                category=request.category,
                priority=request.priority,
            )
        )
    except TicketNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    return TicketResponse.from_ticket(ticket)
