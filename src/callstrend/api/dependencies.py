from functools import lru_cache

from callstrend.application.services.keyword_classifier import KeywordTicketClassifier
from callstrend.application.use_cases import (
    CreateTicketUseCase,
    ListTicketsUseCase,
    UpdateTicketUseCase,
)
from callstrend.infrastructure.repositories.in_memory_ticket_repository import (
    InMemoryTicketRepository,
)


@lru_cache
def get_ticket_repository() -> InMemoryTicketRepository:
    return InMemoryTicketRepository()


@lru_cache
def get_ticket_classifier() -> KeywordTicketClassifier:
    return KeywordTicketClassifier()


def get_create_ticket_use_case() -> CreateTicketUseCase:
    return CreateTicketUseCase(
        ticket_repository=get_ticket_repository(),
        ticket_classifier=get_ticket_classifier(),
    )


def get_list_tickets_use_case() -> ListTicketsUseCase:
    return ListTicketsUseCase(ticket_repository=get_ticket_repository())


def get_update_ticket_use_case() -> UpdateTicketUseCase:
    return UpdateTicketUseCase(ticket_repository=get_ticket_repository())
