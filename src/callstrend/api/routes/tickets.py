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


@router.post("", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
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


@router.get("", response_model=list[TicketResponse])
def list_tickets(
    use_case: Annotated[ListTicketsUseCase, Depends(get_list_tickets_use_case)],
) -> list[TicketResponse]:
    return [TicketResponse.from_ticket(ticket) for ticket in use_case.execute()]


@router.patch("/{ticket_id}", response_model=TicketResponse)
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
