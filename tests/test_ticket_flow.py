from fastapi.testclient import TestClient

from callstrend.api.dependencies import get_ticket_repository
from callstrend.main import app


client = TestClient(app)


def setup_function() -> None:
    get_ticket_repository().clear()


def test_should_create_ticket_with_automatic_classification() -> None:
    response = client.post(
        "/api/v1/tickets",
        json={
            "title": "VPN sem conectar",
            "description": "Estou sem acesso ao sistema interno porque a VPN nao conecta.",
            "requester_name": "Maria Silva",
            "requester_email": "maria@example.com",
        },
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["status"] == "Aberto"
    assert payload["category"] == "Rede"
    assert payload["priority"] == "Alta"
    assert payload["classification_confidence"] >= 0.55


def test_should_list_and_update_ticket() -> None:
    creation_response = client.post(
        "/api/v1/tickets",
        json={
            "title": "Erro no sistema financeiro",
            "description": "O aplicativo apresenta erro ao abrir relatorios.",
            "requester_name": "Joao Souza",
            "requester_email": "joao@example.com",
        },
    )
    ticket_id = creation_response.json()["id"]

    list_response = client.get("/api/v1/tickets")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    update_response = client.patch(
        f"/api/v1/tickets/{ticket_id}",
        json={
            "status": "EmAtendimento",
            "priority": "Media",
        },
    )

    assert update_response.status_code == 200
    payload = update_response.json()
    assert payload["status"] == "EmAtendimento"
    assert payload["priority"] == "Media"
