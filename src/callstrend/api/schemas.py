from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from callstrend.domain.enums import Category, Priority, TicketStatus
from callstrend.domain.models import Ticket


class CreateTicketRequest(BaseModel):
    title: str = Field(min_length=3, max_length=120)
    description: str = Field(min_length=10, max_length=2000)
    requester_name: str = Field(min_length=3, max_length=80)
    requester_email: str = Field(min_length=5, max_length=160)


class UpdateTicketRequest(BaseModel):
    status: TicketStatus | None = None
    category: Category | None = None
    priority: Priority | None = None


class TicketResponse(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    id: str
    title: str
    description: str
    requester_name: str
    requester_email: str
    created_at: datetime
    status: str
    category: str
    priority: str
    classification_confidence: float
    classification_rationale: str

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
