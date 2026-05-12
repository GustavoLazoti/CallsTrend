from collections.abc import Sequence

from callstrend.application.dto import CreateTicketCommand, UpdateTicketCommand
from callstrend.application.exceptions import TicketNotFoundError
from callstrend.domain.models import Ticket
from callstrend.domain.ports import TicketClassifier, TicketRepository


class CreateTicketUseCase:
    def __init__(
        self,
        ticket_repository: TicketRepository,
        ticket_classifier: TicketClassifier,
    ) -> None:
        self._ticket_repository = ticket_repository
        self._ticket_classifier = ticket_classifier

    def execute(self, command: CreateTicketCommand) -> Ticket:
        ticket = Ticket(
            title=command.title.strip(),
            description=command.description.strip(),
            requester_name=command.requester_name.strip(),
            requester_email=command.requester_email.strip().lower(),
        )
        suggestion = self._ticket_classifier.classify(
            title=ticket.title,
            description=ticket.description,
        )
        ticket.apply_classification(suggestion)
        return self._ticket_repository.add(ticket)


class ListTicketsUseCase:
    def __init__(self, ticket_repository: TicketRepository) -> None:
        self._ticket_repository = ticket_repository

    def execute(self) -> Sequence[Ticket]:
        return self._ticket_repository.list_all()


class UpdateTicketUseCase:
    def __init__(self, ticket_repository: TicketRepository) -> None:
        self._ticket_repository = ticket_repository

    def execute(self, command: UpdateTicketCommand) -> Ticket:
        ticket = self._ticket_repository.get_by_id(command.ticket_id)
        if ticket is None:
            raise TicketNotFoundError(command.ticket_id)

        ticket.apply_management_update(
            status=command.status,
            category=command.category,
            priority=command.priority,
        )
        return self._ticket_repository.update(ticket)
