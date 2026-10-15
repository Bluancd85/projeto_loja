# Testes

## Executar

```bash
poetry run pytest
```

Isso já roda com cobertura (configurada em `pyproject.toml`): relatório no
terminal (`term-missing`), relatório HTML em `htmlcov/index.html`, e falha
automaticamente se a cobertura de `src/desafio_aula` ficar abaixo de **75%**.

Para rodar só um arquivo ou um teste específico:

```bash
poetry run pytest tests/test_queries.py
poetry run pytest tests/test_queries.py::test_faturamento_por_pedido -v
```

## Isolamento do banco de dados

Todos os testes usam um banco **SQLite temporário** (`tmp_path`, fixtures em
`tests/conftest.py`), criado a partir do mesmo `data/schema.sql` /
`data/seed.sql` usados em produção. Nenhum teste lê ou escreve em
`data/loja.db` — rodar a suíte de testes nunca afeta o banco real usado pelo
menu interativo.

Fixtures disponíveis:

- `db_path` — caminho de um arquivo de banco temporário (ainda não criado).
- `connection` — conexão com um banco temporário já populado (schema + seed).
- `connection_vazia` — conexão com um banco temporário só com o schema, sem
  dados (útil para testar filtros sem resultado e relatórios vazios).

## O que é coberto

- `test_database.py` — criação do banco, idempotência de `init_db`,
  comportamento de `--reset`, `ensure_db`, e a configuração da conexão
  (`PRAGMA foreign_keys`, `row_factory`).
- `test_queries.py` — cada função de relatório, incluindo casos normais,
  filtros sem resultado e banco vazio.
- `test_main.py` — formatação de cada relatório (vazio e com dados), as
  opções do menu (incluindo entrada inválida) e o laço principal do menu.
