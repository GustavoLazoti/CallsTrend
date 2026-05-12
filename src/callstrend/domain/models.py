from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import uuid4

from callstrend.domain.enums import Category, Priority, TicketStatus


@dataclass(slots=True)
class ClassificationSuggestion:
    category: Category
    priority: Priority
    confidence: float
    rationale: str


@dataclass(slots=True)
class Ticket:
    title: str
    description: str
    requester_name: str
    requester_email: str
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    status: TicketStatus = TicketStatus.EM_TRIAGEM
    category: Category = Category.OUTROS
    priority: Priority = Priority.BAIXA
    classification_confidence: float = 0.0
    classification_rationale: str = "Classificação ainda não executada."

    def apply_classification(self, suggestion: ClassificationSuggestion) -> None:
        self.category = suggestion.category
        self.priority = suggestion.priority
        self.classification_confidence = suggestion.confidence
        self.classification_rationale = suggestion.rationale
        self.status = TicketStatus.ABERTO

    def apply_management_update(
        self,
        *,
        status: TicketStatus | None = None,
        category: Category | None = None,
        priority: Priority | None = None,
    ) -> None:
        if status is not None:
            self.status = status
        if category is not None:
            self.category = category
        if priority is not None:
            self.priority = priority
