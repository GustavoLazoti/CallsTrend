from dataclasses import dataclass

from callstrend.domain.enums import Category, Priority, TicketStatus


@dataclass(slots=True)
class CreateTicketCommand:
    title: str
    description: str
    requester_name: str
    requester_email: str


@dataclass(slots=True)
class UpdateTicketCommand:
    ticket_id: str
    status: TicketStatus | None = None
    category: Category | None = None
    priority: Priority | None = None
