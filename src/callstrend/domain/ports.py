from collections.abc import Sequence
from typing import Protocol

from callstrend.domain.models import ClassificationSuggestion, Ticket


class TicketRepository(Protocol):
    def add(self, ticket: Ticket) -> Ticket: ...

    def list_all(self) -> Sequence[Ticket]: ...

    def get_by_id(self, ticket_id: str) -> Ticket | None: ...

    def update(self, ticket: Ticket) -> Ticket: ...


class TicketClassifier(Protocol):
    def classify(self, *, title: str, description: str) -> ClassificationSuggestion: ...
