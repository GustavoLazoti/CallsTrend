DECLARAÇÃO DE ESCOPO DO PROJETO

1. Identificação do Projeto

Nome do Projeto: Sistema de Help Desk com Triagem Automática de Chamados utilizando Inteligência Artificial
Disciplina: Engenharia de Software
Tipo de Projeto: Projeto acadêmico de desenvolvimento de software

2. Descrição Geral do Escopo

Este documento tem como objetivo definir claramente o escopo do projeto, descrevendo as entregas, funcionalidades, critérios de aceitação, restrições e exclusões.
A Declaração de Escopo estabelece os limites do projeto, garantindo alinhamento entre as expectativas do aluno desenvolvedor e os critérios de avaliação da disciplina, evitando ambiguidades e expansão não controlada do escopo (scope creep).

3. Entregas do Projeto (Deliverables)

3.1 Entregas Principais

Documento TAP (Termo de Abertura do Projeto) Cronograma inicial com marcos (Gantt) Declaração de Escopo Estrutura Analítica do Projeto (EAP / WBS) Documento de Requisitos Funcionais e Não Funcionais Diagramas do sistema (casos de uso, classes e arquitetura) Protótipo funcional do sistema de Help Desk Módulo de Triagem Automática de Chamados com IA Relatório de testes e validação Documentação final do projeto 

4. Funcionalidades e Requisitos do Sistema

4.1 Requisitos Funcionais

RF01 – Permitir cadastro e autenticação de usuários RF02 – Permitir abertura de chamados com descrição textual RF03 – Classificar automaticamente chamados por categoria utilizando IA RF04 – Classificar automaticamente chamados por nível de prioridade RF05 – Permitir visualização e acompanhamento do status do chamado RF06 – Permitir que administradores visualizem e gerenciem chamados RF07 – Permitir atualização do status do chamado (aberto, em andamento, resolvido) 

4.2 Requisitos Não Funcionais

RNF01 – O sistema deve possuir interface simples e intuitiva RNF02 – O tempo de resposta da triagem automática deve ser adequado para uso acadêmico RNF03 – O sistema deve ser desenvolvido utilizando tecnologias gratuitas ou open-source RNF04 – O sistema deve ser acessível via navegador web RNF05 – O código-fonte deve seguir boas práticas de organização e versionamento 

5. Critérios de Aceitação

5.1 Critérios Gerais

Todas as funcionalidades descritas nos requisitos funcionais devem estar implementadas O sistema deve permitir a abertura e triagem automática de chamados O módulo de IA deve classificar chamados de forma demonstrável O sistema deve estar funcional em ambiente local ou acadêmico A documentação exigida pela disciplina deve estar completa e organizada 

5.2 Critérios de Aceitação da Triagem Automática

O sistema deve atribuir automaticamente uma categoria ao chamado O sistema deve atribuir automaticamente uma prioridade ao chamado A classificação deve ser visível para o usuário e para o administrador O funcionamento da triagem deve ser demonstrável durante apresentação ou demo 

6. Restrições do Projeto

O projeto será desenvolvido por um único aluno O prazo de desenvolvimento está limitado ao semestre letivo Não haverá investimento financeiro no projeto A base de dados utilizada será simulada ou reduzida O sistema será desenvolvido exclusivamente para fins acadêmicos 

7. Exclusões do Escopo (Fora do Escopo)

Integração com sistemas corporativos reais (ex: ServiceNow, Jira) Envio de notificações por e-mail, SMS ou aplicativos externos Implementação de SLAs reais ou contratos de atendimento Uso do sistema em ambiente de produção Autenticação avançada (SSO, OAuth corporativo) Monitoramento em tempo real ou alta disponibilidade 

8. Premissas

O usuário fornecerá corretamente as informações do chamado O módulo de IA terá caráter demonstrativo, não comercial O ambiente de execução será local ou acadêmico O professor atuará como avaliador e cliente do projeto 

9. Controle de Escopo

Qualquer solicitação de alteração no escopo deverá ser avaliada considerando o impacto no prazo e nas entregas do projeto, podendo ser recusada caso comprometa os objetivos acadêmicos estabelecidos nesta Declaração de Escopo.


## 1. Diagrama de Classes

```mermaid
classDiagram
direction LR

class Usuario {
  +UUID id
  +string nome
  +string email
  +string senhaHash
  +autenticar(email, senha)
  +abrirChamado(titulo, descricao)
  +consultarChamados()
}

class Administrador {
  +validarClassificacao(chamadoId)
  +corrigirCategoria(chamadoId, categoria)
  +corrigirPrioridade(chamadoId, prioridade)
  +alterarStatus(chamadoId, status)
  +visualizarPainel()
}

Usuario <|-- Administrador

class Chamado {
  +UUID id
  +string titulo
  +string descricao
  +datetime dataHoraAbertura
  +StatusChamado status
  +Categoria categoria
  +Prioridade prioridade
  +registrar()
  +atualizarStatus(status)
  +atualizarClassificacao(categoria, prioridade)
}

class ClassificacaoIA {
  +Categoria categoriaSugerida
  +Prioridade prioridadeSugerida
  +float confianca
  +datetime dataHoraClassificacao
}

class LogClassificacao {
  +UUID id
  +datetime dataHora
  +string textoEntrada
  +Categoria categoriaGerada
  +Prioridade prioridadeGerada
  +float tempoProcessamento
  +string observacao
}

class Backend {
  +abrirChamado(usuarioId, titulo, descricao)
  +solicitarTriagem(texto)
  +salvarChamado(chamado)
  +autenticarUsuario(email, senha)
  +atualizarChamado(chamadoId, dados)
}

class ModuloIA {
  +classificarChamado(titulo, descricao)
  +processarTexto(texto)
}

class AutenticacaoService {
  +login(email, senha)
  +gerarHash(senha)
  +validarSenha(senha, hash)
}

class UsuarioRepository {
  +salvar(usuario)
  +buscarPorEmail(email)
  +buscarPorId(id)
}

class ChamadoRepository {
  +salvar(chamado)
  +buscarPorId(id)
  +listarPorUsuario(usuarioId)
  +atualizar(chamado)
}

class LogRepository {
  +salvar(log)
}

class Categoria {
  <<enumeration>>
  Hardware
  Software
  Rede
  Acesso
  Outros
}

class Prioridade {
  <<enumeration>>
  Baixa
  Media
  Alta
}

class StatusChamado {
  <<enumeration>>
  Aberto
  EmTriagem
  EmAtendimento
  Resolvido
  Fechado
}

Usuario "1" --> "0..*" Chamado : abre
Chamado "1" --> "0..1" ClassificacaoIA : possui
Chamado "1" --> "0..*" LogClassificacao : gera

Backend --> ModuloIA : solicita classificação
Backend --> ChamadoRepository : persiste chamado
Backend --> UsuarioRepository : consulta usuário
Backend --> LogRepository : registra logs
Backend --> AutenticacaoService : autentica

ModuloIA --> ClassificacaoIA : produz
AutenticacaoService --> Usuario : valida acesso
Administrador --> Chamado : gerencia
```

### Refinamentos aplicados
- **Administrador herda de Usuario**, como você pediu.
- A **IA não substitui o backend**: ela é um módulo isolado, chamado pela classe `Backend`.
- A entidade `ClassificacaoIA` foi separada do `Chamado` para deixar explícita a origem da classificação automática.
- `LogClassificacao` ajuda a justificar a camada de dados e auditoria da IA.
- Foram incluídos enums de **Categoria**, **Prioridade** e **StatusChamado** para fortalecer a modelagem.

---

## 2. Diagrama de Sequência

Fluxo principal: abertura de chamado com triagem automática por IA.

```mermaid
sequenceDiagram
autonumber
actor U as Usuário Final
participant W as Interface Web
participant B as Backend
participant IA as Módulo de IA
participant DB as Banco de Dados
actor A as Administrador

U->>W: Preenche título e descrição do chamado
W->>B: enviarChamado(titulo, descricao, usuarioId)

B->>B: validarDados()
B->>DB: registrar chamado(status=EmTriagem, dataHoraAbertura)
DB-->>B: chamadoId

B->>IA: classificarChamado(titulo, descricao)
IA->>IA: processarTexto()
IA-->>B: categoria, prioridade, confiança

B->>B: associarClassificacaoAoChamado()
B->>DB: atualizar chamado(categoria, prioridade, status=Aberto)
B->>DB: salvar log de classificação
DB-->>B: confirmação

B-->>W: chamado registrado com classificação automática
W-->>U: exibir número, categoria e prioridade

A->>W: acessar painel administrativo
W->>B: listar chamados()
B->>DB: consultar chamados
DB-->>B: lista de chamados
B-->>W: retornar chamados

A->>W: corrigir classificação / alterar status
W->>B: atualizarChamado(chamadoId, status, categoria, prioridade)
B->>DB: persistir alterações
DB-->>B: confirmação
B-->>W: atualização concluída
W-->>A: exibir sucesso
```

### Pontos fortes deste fluxo
- Mostra claramente que o **backend coordena tudo**.
- O chamado pode ser criado inicialmente com status **EmTriagem** e depois atualizado para **Aberto** após resposta da IA.
- O administrador entra depois para **validar/corrigir** a sugestão da IA.

---

## 3. Diagrama de Atividades

Fluxo de abertura e tratamento do chamado com decisão sobre ajuste administrativo.

```mermaid
flowchart TD
    A[Início] --> B[Usuário autentica no sistema]
    B --> C[Acessa formulário de abertura]
    C --> D[Informa título e descrição]
    D --> E[Backend valida dados]
    E --> F[Registrar chamado com data/hora e status EmTriagem]
    F --> G[Enviar título e descrição ao Módulo de IA]
    G --> H[IA processa texto]
    H --> I[Retornar categoria e prioridade sugeridas]
    I --> J[Backend salva classificação e log]
    J --> K[Atualizar chamado para status Aberto]
    K --> L[Exibir resultado ao usuário]

    L --> M{Administrador irá revisar?}
    M -- Não --> N[Fim]
    M -- Sim --> O[Administrador acessa painel]
    O --> P[Visualiza chamado e sugestão da IA]
    P --> Q{Classificação está correta?}
    Q -- Sim --> R[Administrador altera apenas status se necessário]
    Q -- Não --> S[Administrador corrige categoria e/ou prioridade]
    R --> T[Salvar alterações]
    S --> T
    T --> N[Fim]
```

### Observações
- Esse diagrama enfatiza bem o **processo de negócio**.
- A revisão administrativa ficou opcional, o que combina com sua proposta de triagem automática.
- O ponto de integração com IA aparece de forma objetiva.

---

## 4. Diagrama de Componentes

Modelagem da arquitetura em 4 camadas, com destaque para a integração Backend ↔ IA.

```mermaid
flowchart LR
    subgraph AP[Camada de Apresentação]
        UI[Interface Web]
        ADM[Painel Administrativo]
    end

    subgraph APP[Camada de Aplicação / Backend]
        AUTH[Serviço de Autenticação]
        CHAM[Serviço de Chamados]
        ORQ[Orquestrador de Triagem]
        API[API Backend]
    end

    subgraph IA[Camada de Inteligência Artificial]
        NLP[Módulo de Processamento de Linguagem Natural]
        CLASS[Motor de Classificação\nCategoria + Prioridade]
    end

    subgraph DADOS[Camada de Dados]
        USERDB[(Tabela Usuários)]
        TICKETDB[(Tabela Chamados)]
        LOGDB[(Tabela Logs de Classificação)]
    end

    UI --> API
    ADM --> API

    API --> AUTH
    API --> CHAM
    CHAM --> ORQ
    ORQ --> NLP
    NLP --> CLASS
    CLASS --> ORQ

    AUTH --> USERDB
    CHAM --> TICKETDB
    ORQ --> LOGDB
    ORQ --> TICKETDB
```

### O que este diagrama deixa claro
- A **Interface Web** e o **Painel Administrativo** consomem a **API Backend**.
- O **Backend** contém autenticação, gestão de chamados e um **orquestrador** para a triagem.
- O **Módulo de IA** está isolado, mas conectado ao backend.
- O backend persiste tanto o chamado quanto os **logs da classificação**.

---

## Sugestões de melhoria para sua entrega acadêmica

Se você quiser deixar os diagramas ainda mais consistentes com documentação formal, recomendo:

1. **Padronizar nomes dos status**
   - Ex.: `Aberto`, `Em Triagem`, `Em Atendimento`, `Resolvido`, `Fechado`.

2. **Adicionar confiança da IA**
   - Isso enriquece a justificativa de por que o administrador pode revisar uma classificação.

3. **Explicitar restrição de desempenho**
   - No texto do trabalho, cite que o módulo de IA deve responder em até **3 segundos**.
   - Em alguns casos, isso pode aparecer como nota no diagrama de componentes.

4. **Manter a segurança fora do diagrama de classes principal**
   - A autenticação pode aparecer como serviço, sem poluir demais a modelagem de domínio.

---

## Versão resumida da interpretação conceitual

- **Classes**: modelam entidades e serviços.
- **Sequência**: mostra a ordem da abertura do chamado e da triagem automática.
- **Atividades**: representa o fluxo operacional do processo.
- **Componentes**: evidencia a arquitetura em 4 camadas.

Descrição do Projeto para Refinamento de Modelagem
Título: Sistema de Help Desk com Triagem Automática de Chamados (IA).
1. Objetivo Geral:
Desenvolver uma ferramenta acadêmica de Help Desk que utilize Inteligência Artificial para otimizar o fluxo de atendimento. O foco principal é a triagem automática, que elimina a necessidade de classificação manual imediata por parte do administrador.  
2. Atores e Personas:
• Usuário Final: Funcionário que abre chamados técnicos para resolver problemas rapidamente.  
• Administrador: Responsável por gerenciar o volume de chamados, podendo validar ou corrigir a IA.  
• Sistema de IA: Atua como um ator interno que realiza o processamento textual para classificação.  
3. Requisitos Funcionais Chave:
• Abertura e Triagem (RF03/RF04): O usuário fornece título e descrição; o sistema registra data/hora e executa o módulo de IA.  
• Classificação por IA: O sistema deve atribuir automaticamente uma Categoria e um nível de Prioridade (Baixa, Média, Alta).  
• Gestão Administrativa (RF06): O administrador tem o poder de alterar o status do chamado e ajustar as classificações sugeridas pela IA.  
4. Arquitetura do Sistema (4-Tier):
• Apresentação: Interface Web para interação do usuário e painéis administrativos.  
• Aplicação (Backend): Camada de lógica de negócio, controle de autenticação e ponte para o módulo de IA.  
• Inteligência Artificial: Módulo isolado de processamento de linguagem natural para classificação textual.  
• Dados: Banco de dados relacional para persistência de usuários, chamados e logs.  
5. Regras de Negócio e Restrições Técnicas:
• Segurança: Autenticação obrigatória com senhas criptografadas via algoritmos de hash (ex: bcrypt).  
• Desempenho: A triagem pela IA deve ocorrer em no máximo 3 segundos.  
• Escopo: O sistema é focado em ambiente acadêmico, sem integrações externas (como e-mail ou Slack) nesta fase.
