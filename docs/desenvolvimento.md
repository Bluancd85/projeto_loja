# Desenvolvimento

## Lint e formatação

O **Ruff** é a única ferramenta de lint e formatação do projeto. Lint e
format são tasks separadas (via Poe the Poet):

```bash
poetry run task lint     # ruff check . — identifica problemas, não reformata
poetry run task format   # ruff format . — aplica a formatação padrão
```

Fluxo recomendado antes de qualquer commit:

```bash
poetry run task lint
poetry run task format
poetry run task lint
```

Se `poetry run task lint` não for reconhecido, use `poetry run poe lint`
como alternativa.

## Testes e cobertura

Veja [Testes](testes.md).

## Documentação

```bash
poetry run mkdocs serve   # preview local em http://127.0.0.1:8000
poetry run mkdocs build   # build estático em site/ (falha em nav/links quebrados)
```

## Contribuindo

- Siga o layout `src/desafio_aula/` para qualquer novo módulo de código.
- Toda nova consulta de relatório entra em `queries.py` (SQL puro, devolve
  `sqlite3.Row`); a formatação para o usuário entra em `main.py`.
- Toda alteração de schema entra em `data/schema.sql`; dados de exemplo
  adicionais entram em `data/seed.sql`.
- Mudanças de comportamento público devem atualizar esta documentação.
