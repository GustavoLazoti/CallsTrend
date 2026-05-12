from enum import StrEnum


class Category(StrEnum):
    HARDWARE = "Hardware"
    SOFTWARE = "Software"
    REDE = "Rede"
    ACESSO = "Acesso"
    OUTROS = "Outros"


class Priority(StrEnum):
    BAIXA = "Baixa"
    MEDIA = "Media"
    ALTA = "Alta"


class TicketStatus(StrEnum):
    EM_TRIAGEM = "EmTriagem"
    ABERTO = "Aberto"
    EM_ATENDIMENTO = "EmAtendimento"
    RESOLVIDO = "Resolvido"
    FECHADO = "Fechado"
