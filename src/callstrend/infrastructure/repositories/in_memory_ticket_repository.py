from copy import deepcopy

from callstrend.domain.models import Ticket
from callstrend.domain.ports import TicketRepository


class InMemoryTicketRepository(TicketRepository):
    def __init__(self) -> None:
        self._tickets: dict[str, Ticket] = {}

    def add(self, ticket: Ticket) -> Ticket:
        self._tickets[ticket.id] = deepcopy(ticket)
        return deepcopy(ticket)

    def list_all(self) -> list[Ticket]:
        return [deepcopy(ticket) for ticket in self._tickets.values()]

    def get_by_id(self, ticket_id: str) -> Ticket | None:
        ticket = self._tickets.get(ticket_id)
        return deepcopy(ticket) if ticket is not None else None

    def update(self, ticket: Ticket) -> Ticket:
        self._tickets[ticket.id] = deepcopy(ticket)
        return deepcopy(ticket)

    def clear(self) -> None:
        self._tickets.clear()
