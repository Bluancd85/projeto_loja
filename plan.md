# Plano — Mini Loja (CLI Python + SQLite)

## Contexto

O desafio ([.claude/DESAFIO.md](.claude/DESAFIO.md)) pede uma aplicação de linha de comando que simula relatórios de uma loja virtual: banco **SQLite** com 4 tabelas relacionadas (clientes, produtos, pedidos, itens_pedido) e um menu de terminal com relatórios (produtos por categoria, pedidos detalhados via JOIN, faturamento por cliente/categoria/pedido, ranking de produtos mais vendidos).

O README embutido no próprio DESAFIO.md sugere `requirements.txt` + `venv` manual + `src/` sem sub-pacote. Este workspace já adota o padrão de engenharia definido em [.claude/skills/python-project-standards/SKILL.md](.claude/skills/python-project-standards/SKILL.md) (pyenv + Poetry + Ruff + Poe the Poet + Pytest/pytest-cov ≥75% + MkDocs Material, layout `src/<pacote>`). Este plano usa o **domínio e os requisitos funcionais do DESAFIO.md**, mas substitui integralmente as instruções de ferramentas do README do desafio (requirements.txt, venv manual) pelo fluxo da skill — é esse fluxo que será documentado no README final, não o do DESAFIO.md.

O esqueleto já existe parcialmente neste repositório: `pyproject.toml` (nome `desafio-aula`, `requires-python = ">=3.14"`, pacote `desafio_aula` em `src/`), `src/desafio_aula/__init__.py`, `tests/__init__.py`. O plano constrói sobre esse esqueleto em vez de recomeçar — mantém o nome do pacote `desafio_aula`.

## Decisões de mapeamento (DESAFIO.md → padrão da skill)

| DESAFIO.md | Neste projeto |
|---|---|
| `requirements.txt` + `venv` manual | Poetry + pyenv (`.venv/` gerenciado pelo Poetry) |
| `src/database.py`, `src/queries.py`, `src/main.py` na raiz de `src/` | movidos para dentro do pacote: `src/desafio_aula/database.py`, `queries.py`, `main.py` |
| `python src/main.py` | `poetry run python -m desafio_aula.main` (e, como bônus, script `poetry run desafio-aula`) |
| `pytest -v` direto | `poetry run pytest` (config central em `pyproject.toml`, cobertura ≥75%) |
| sem lint/format/docs | Ruff + tasks do Poe + MkDocs Material, conforme SKILL.md |
| `data/schema.sql`, `data/seed.sql`, `data/loja.db` | mantidos como estão (ativos de dados estáticos/gerados, fora do pacote Python — não seguem o layout `src/`, apenas são lidos por `database.py`) |

## Passo a passo

1. **Ambiente** (Seção 4 da skill): `pyenv install`/`pyenv local` com uma versão estável compatível com `requires-python = ">=3.14"` do `pyproject.toml`; `poetry config virtualenvs.in-project true --local`; `poetry env use "$(pyenv which python)"`; `poetry install`.
2. **Dependências**: nenhuma dependência de runtime extra (`sqlite3` é stdlib). Dev: `ruff`, `poethepoet`, `pytest`, `pytest-cov`, `mkdocs`, `mkdocs-material` (Seções 6–8 da skill).
3. **Dados**: `data/schema.sql` (CREATE TABLE clientes/produtos/pedidos/itens_pedido + PK/FK + ao menos uma VIEW de relatório) e `data/seed.sql` (dados de exemplo plausíveis).
4. **Código** (`src/desafio_aula/`):
   - `database.py` — conexão sqlite3, criação do banco a partir de `data/schema.sql`, população via `data/seed.sql`, flag `--reset`, criação automática se o banco não existir.
   - `queries.py` — uma função por relatório: lista de produtos (com filtro por categoria), pedidos detalhados (JOIN clientes/pedidos/itens/produtos), faturamento por cliente, por categoria e por pedido, ranking de produtos mais vendidos.
   - `main.py` — menu de terminal que chama as funções de `queries.py`; `main()` + guarda `if __name__ == "__main__":`.
5. **Testes** (`tests/`): `conftest.py` com fixture de banco **temporário** (schema+seed aplicados em arquivo/memória isolada, nunca o `data/loja.db` real); `test_database.py` e `test_queries.py` cobrindo casos normais, limites, filtros sem resultado e entradas inválidas. Meta: ≥75% de cobertura sobre `src/desafio_aula`.
6. **Qualidade**: configurar `[tool.ruff]`, `[tool.ruff.lint]`, `[tool.poe.tasks]` (`lint`/`format`) no `pyproject.toml`; rodar `lint → format → lint`.
7. **Documentação**: `mkdocs.yml` + `docs/{index,instalacao,uso,arquitetura,desenvolvimento,testes}.md` com conteúdo específico da Mini Loja (não genérico) — propósito, setup via pyenv/Poetry, como popular o banco e rodar o menu, como testar/cobrir, como lintar/formatar, como gerar os docs.
8. **README.md** (hoje vazio/corrompido): reescrever com as instruções reais baseadas em Poetry, substituindo o fluxo de `requirements.txt`/venv manual do DESAFIO.md.
9. **`.gitignore`** (ainda não existe): excluir `.venv/`, `__pycache__/`, `*.pyc`, `.pytest_cache/`, `.ruff_cache/`, `htmlcov/`, `.coverage`, `dist/`, `build/`, `site/`, `data/loja.db`.
10. **Fluxo de validação obrigatório** (Seção 10 da skill): `python --version`, `pyenv version`, `poetry env info`, `poetry install`, `task lint → format → lint`, `pytest` (com `--cov-fail-under=75`), `mkdocs build` — executar de ponta a ponta e corrigir qualquer falha antes de considerar concluído.

## Arquivos a criar/alterar

- `pyproject.toml` — estender com dev deps, `[tool.ruff]`, `[tool.ruff.lint]`, `[tool.pytest.ini_options]`, `[tool.poe.tasks]`, `[tool.poetry.scripts]`.
- `.python-version`, `.gitignore` (novos).
- `data/schema.sql`, `data/seed.sql` (novos; `data/loja.db` é gerado, não versionado).
- `src/desafio_aula/database.py`, `queries.py`, `main.py` (novos).
- `tests/conftest.py`, `test_database.py`, `test_queries.py` (novos).
- `mkdocs.yml`, `docs/index.md`, `docs/instalacao.md`, `docs/uso.md`, `docs/arquitetura.md`, `docs/desenvolvimento.md`, `docs/testes.md` (novos).
- `README.md` (reescrever).

## Verificação

- Executar o fluxo da Seção 10 do SKILL.md de ponta a ponta nesta sessão e relatar resultados reais (sem presumir sucesso).
- Rodar o menu manualmente (`poetry run python -m desafio_aula.main`) e confirmar que todos os relatórios exigidos pelo DESAFIO.md funcionam: produtos (com e sem filtro de categoria), pedidos detalhados, faturamento por cliente/categoria/pedido, ranking de produtos.
- Conferir a checklist final da Seção 14 do SKILL.md item a item antes de considerar o projeto pronto.
