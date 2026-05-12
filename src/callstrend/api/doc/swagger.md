# Swagger — CallsTrend API

Professor, como as API's são 'middle' entre a interface que o usuário cadastra e o backend, não será tratado aqui questões de autênticação, isso será realizado na próxima camada.
Em adição, apesar de complexo de desenvolver, é direto ao ponto, ou seja, não tem necessidade de diversos endpoints já que os presentes aqui são suficiêntes para as atuações principais;

## Enums
Abaixo, algumas categorias inicialmente pensadas para retorno de IA, imaginando um uso coorporativo.

| Campo | Valores |
|---|---|
| `category` | `Hardware`, `Software`, `Rede`, `Acesso`, `Outros` |
| `priority` | `Baixa`, `Media`, `Alta` |
| `status` | `EmTriagem`, `Aberto`, `EmAtendimento`, `Resolvido`, `Fechado` |

## Endpoints

### GET `/health`

Verifica disponibilidade da API, simples assim.

Response 200
```json
{
  "status": "ok"
}
```

---

### POST `/api/v1/tickets`

Cria chamado e executa classificação automática.

Request body
```json
{
  "title": "VPN sem conectar",
  "description": "Não consigo acessar o sistema interno pela VPN desde a manhã.",
  "requester_name": "Maria Silva",
  "requester_email": "maria@empresa.com"
}
```

Response 201
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "title": "VPN sem conectar",
  "description": "Não consigo acessar o sistema interno pela VPN desde a manhã.",
  "requester_name": "Maria Silva",
  "requester_email": "maria@empresa.com",
  "created_at": "2026-05-12T21:00:00Z",
  "status": "Aberto",
  "category": "Rede",
  "priority": "Alta",
  "classification_confidence": 0.83,
  "classification_rationale": "Categoria sugerida: Rede (score 2). Prioridade sugerida: Alta (score 2)."
}
```

Códigos
- `201` criado com sucesso
- `422` validação inválida

---

### GET `/api/v1/tickets`

Lista todos os chamados.

Response 200
```json
[
  {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "title": "VPN sem conectar",
    "description": "Não consigo acessar o sistema interno pela VPN desde a manhã.",
    "requester_name": "Maria Silva",
    "requester_email": "maria@empresa.com",
    "created_at": "2026-05-12T21:00:00Z",
    "status": "Aberto",
    "category": "Rede",
    "priority": "Alta",
    "classification_confidence": 0.83,
    "classification_rationale": "Categoria sugerida: Rede (score 2). Prioridade sugerida: Alta (score 2)."
  }
]
```

---

### PATCH `/api/v1/tickets/{ticket_id}`

Atualiza status/categoria/prioridade de um chamado.

Request body (campos opcionais)
```json
{
  "status": "EmAtendimento",
  "category": "Rede",
  "priority": "Alta"
}
```

**Response 200**
- Retorna `TicketResponse` atualizado.

**Códigos**
- `200` atualizado com sucesso
- `404` chamado não encontrado
- `422` validação inválida

