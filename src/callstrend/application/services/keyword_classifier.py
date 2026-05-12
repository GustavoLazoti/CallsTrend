from __future__ import annotations

from collections.abc import Iterable
from typing import TypeVar

from callstrend.domain.enums import Category, Priority
from callstrend.domain.models import ClassificationSuggestion
from callstrend.domain.ports import TicketClassifier


TEnum = TypeVar("TEnum")


class KeywordTicketClassifier(TicketClassifier):
    _category_keywords: dict[Category, tuple[str, ...]] = {
        Category.HARDWARE: ("teclado", "monitor", "notebook", "mouse", "impressora", "hardware"),
        Category.SOFTWARE: ("erro", "sistema", "app", "aplicativo", "instalar", "software"),
        Category.REDE: ("rede", "internet", "wifi", "vpn", "conexao", "latencia"),
        Category.ACESSO: ("senha", "login", "acesso", "permissao", "bloqueado", "autenticacao"),
    }
    _priority_keywords: dict[Priority, tuple[str, ...]] = {
        Priority.ALTA: ("urgente", "critico", "parado", "indisponivel", "bloqueado", "sem acesso"),
        Priority.MEDIA: ("lento", "intermitente", "instavel", "falhando"),
        Priority.BAIXA: ("duvida", "ajuda", "orientacao", "melhoria"),
    }

    def classify(self, *, title: str, description: str) -> ClassificationSuggestion:
        normalized_title = title.lower()
        normalized_description = description.lower()
        text = f"{normalized_title} {normalized_description}"

        category, category_score = self._best_match(
            normalized_title,
            normalized_description,
            self._category_keywords,
            Category.OUTROS,
        )
        priority, priority_score = self._best_match(
            normalized_title,
            normalized_description,
            self._priority_keywords,
            Priority.BAIXA,
        )

        confidence = min(0.55 + (category_score * 0.12) + (priority_score * 0.08), 0.95)
        rationale = self._build_rationale(category, priority, category_score, priority_score)

        return ClassificationSuggestion(
            category=category,
            priority=priority,
            confidence=round(confidence, 2),
            rationale=rationale,
        )

    def _best_match(
        self,
        title: str,
        description: str,
        keyword_map: dict[TEnum, tuple[str, ...]],
        fallback: TEnum,
    ) -> tuple[TEnum, int]:
        ranked_matches = [
            (enum_value, self._count_matches(title, description, keywords))
            for enum_value, keywords in keyword_map.items()
        ]
        ranked_matches.sort(key=lambda item: item[1], reverse=True)
        best_value, best_score = ranked_matches[0]
        if best_score == 0:
            return fallback, 0
        return best_value, best_score

    @staticmethod
    def _count_matches(title: str, description: str, keywords: Iterable[str]) -> int:
        score = 0
        for keyword in keywords:
            if keyword in title:
                score += 2
            if keyword in description:
                score += 1
        return score

    @staticmethod
    def _build_rationale(
        category: Category,
        priority: Priority,
        category_score: int,
        priority_score: int,
    ) -> str:
        if category_score == 0 and priority_score == 0:
            return (
                "Nenhuma palavra-chave forte foi encontrada; o chamado recebeu "
                "classificação padrão para permitir continuidade do fluxo."
            )

        return (
            f"Categoria sugerida: {category.value} (score {category_score}). "
            f"Prioridade sugerida: {priority.value} (score {priority_score})."
        )
