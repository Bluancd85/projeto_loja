# Mini Loja

Aplicação de linha de comando que simula os relatórios de uma pequena loja
virtual. Os dados ficam em um banco **SQLite** (`data/loja.db`) com quatro
tabelas relacionadas — `clientes`, `produtos`, `pedidos` e `itens_pedido` — e
são consultados a partir de um menu de terminal escrito em **Python**.

## O que o projeto faz

- Cria o banco de dados a partir de `data/schema.sql` (tabelas, chaves
  primárias/estrangeiras e uma view de relatório) e o popula com dados de
  exemplo a partir de `data/seed.sql`.
- Oferece um menu interativo no terminal com os seguintes relatórios:
  - Lista de produtos, com filtro opcional por categoria.
  - Pedidos detalhados, juntando cliente, pedido, item e produto (`JOIN`).
  - Faturamento agrupado por cliente, por categoria e por pedido.
  - Ranking dos produtos mais vendidos por quantidade.

## Modelo de dados

```text
clientes (1) ──< pedidos (1) ──< itens_pedido >── (1) produtos
```

- Um **cliente** faz vários **pedidos**.
- Um **pedido** contém vários **itens**.
- Cada **item** aponta para um **produto**.

## Stack de engenharia

Este projeto segue o padrão de engenharia Python do curso: **pyenv** (versão
local do interpretador), **Poetry** (dependências e ambiente virtual),
**Ruff** (lint e formatação), **Pytest + pytest-cov** (testes com cobertura
mínima de 75%) e **MkDocs Material** (esta documentação). Veja
[Instalação](instalacao.md) para colocar o projeto em funcionamento.
