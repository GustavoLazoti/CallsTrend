class TicketNotFoundError(Exception):
    def __init__(self, ticket_id: str) -> None:
        super().__init__(f"Chamado '{ticket_id}' não encontrado.")
        self.ticket_id = ticket_id
