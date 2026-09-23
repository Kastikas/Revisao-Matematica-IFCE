---
name: gestao-planos-progresso
description: >-
  Use esta skill sempre que criar, atualizar ou retomar planos de implementação,
  migrações, auditorias ou novos blocos de provas no projeto PartiuIF. Define a
  metodologia de checkpointing atômico e recuperação contra interrupções para economizar recursos.
---

# Gestão de Planos, Checkpoints e Persistência de Progresso

Esta skill padroniza como planejamentos de longo prazo e tarefas em lote (como ingestão de novas provas, auditoria de imagens e refatorações) são documentados, rastreados e retomados em caso de interrupção ou falha, garantindo **resiliência e economia de tokens e chamadas de API**.

---

## 1. Estrutura de Diretórios Padronizada

Todos os documentos de planejamento e registros de estado residem exclusivamente na pasta `planos/`:

```text
planos/
├── <nome_tarefa>.md           # Documento de planejamento estratégico e arquitetural
└── progresso/
    └── <nome_tarefa>_progresso.json # Arquivo de checkpoint de estado legível por máquina
```

---

## 2. O Ciclo de Vida do Trabalho (Metodologia de 4 Fases)

### Fase 1: Elaboração do Plano Estratégico (`planos/<tarefa>.md`)
Antes de iniciar uma tarefa multi-etapa ou em lote, crie um plano markdown em `planos/<tarefa>.md` contendo:
1. **Objetivo Claro:** O que será entregue (ex.: "Implementação das Provas do IFRN de 2020 a 2025").
2. **Escopo e Fases:** Decomposição em lotes ou marcos sequenciais bem definidos.
3. **Critérios de Aceite:** Regras de KaTeX, acessibilidade de imagens, schema e validação de DOM.

### Fase 2: Inicialização do Checkpoint (`planos/progresso/<tarefa>_progresso.json`)
Crie o arquivo JSON de estado granular com todas as etapas marcadas como `PENDING`.
Exemplo canônico:
```json
{
  "task_id": "implementacao_ifxx",
  "title": "Implementação Provas IFXX",
  "status": "IN_PROGRESS",
  "last_updated": "2026-09-22T12:00:00-03:00",
  "stages": {
    "etapa_1_infra": { "status": "PENDING" },
    "etapa_2_questoes": {
      "status": "IN_PROGRESS",
      "items": {
        "ifxx-2025-1": { "status": "DONE", "questions": 15, "images": 4 },
        "ifxx-2024-1": { "status": "PENDING", "questions": 15, "images": 5 }
      }
    },
    "etapa_3_validacao": { "status": "PENDING" },
    "etapa_4_compilacao": { "status": "PENDING" }
  }
}
```

### Fase 3: Gravação Atômica a Cada Marco Concluído
- A cada exame, lote de imagens ou validação concluída, **atualize imediatamente** o campo de status correspondente para `DONE` e registre `last_updated`.
- Nunca acumule múltiplas fases sem registrar o checkpoint no JSON.

### Fase 4: Retomada Instantânea e Resiliente (Recuperação de Falhas)
Sempre que uma tarefa for retomada (após interrupção do usuário, estouro de contexto, reinício de servidor ou início de uma nova sessão):
1. **Primeiro Passo Obrigatório:** Inspecione `planos/progresso/<tarefa>_progresso.json`.
2. **Identifique a Fronteira:** Localize o primeiro item com status `IN_PROGRESS` ou `PENDING`.
3. **Pule o que já está `DONE`:** Nunca re-extraia imagens ou re-processe questões já marcadas como `DONE`. Retome a execução estritamente a partir do ponto onde parou.
4. **Economia de Recursos:** Essa leitura inicial leva menos de 10 ms e economiza dezenas de chamadas de ferramentas e milhares de tokens.

---

## 3. Diretrizes de Integração com o Tooling Centralizado

- Qualquer novo dado estruturado deve passar pelo [`scripts/manage_mathdata.py`](file:///home/ivanlrk/Projetos/revisao-site-ifce/scripts/manage_mathdata.py):
  ```bash
  python3 scripts/manage_mathdata.py import -f caminho/prova.json -b <bloco_id> --build
  ```
- A finalização de um marco no checkpoint só deve ser marcada como `DONE` após a validação bem-sucedida:
  ```bash
  python3 scripts/manage_mathdata.py validate
  ```
