# Arquitetura

## Estrutura de pastas

```text
desafio_aula/
├── data/
│   ├── schema.sql      # tabelas, PK/FK e a view vw_itens_detalhados
│   └── seed.sql        # dados de exemplo
├── src/desafio_aula/
│   ├── database.py     # conexão sqlite3, criação/reset do banco, CLI --reset
│   ├── queries.py       # uma função por relatório
│   └── main.py          # menu de terminal
└── tests/               # testes automatizados (pytest)
```

## Decisões

- **Layout `src/`**: o pacote `desafio_aula` vive em `src/`, nunca na raiz do
  repositório, conforme o padrão de engenharia do curso. O código de domínio
  do desafio original (`database.py`, `queries.py`, `main.py`, que no
  DESAFIO.md ficariam direto em `src/`) foi movido para dentro do pacote.
- **View `vw_itens_detalhados`** (em `data/schema.sql`): uma única view junta
  `clientes`, `pedidos`, `itens_pedido` e `produtos` e calcula o subtotal de
  cada item (`quantidade * preco_unitario`). Todas as consultas de
  `queries.py` que precisam de dados de mais de uma tabela (pedidos
  detalhados, faturamento por cliente/categoria/pedido, ranking de produtos)
  reaproveitam essa view em vez de repetir os mesmos `JOIN`s em cada consulta.
- **Separação `queries.py` / `main.py`**: `queries.py` só executa SQL e
  devolve `sqlite3.Row`; `main.py` formata esse resultado em texto e cuida da
  interação com o usuário (menu, leitura de `input`). Essa separação permite
  testar a formatação e as consultas isoladamente, sem simular entrada de
  teclado.
- **`database.py` idempotente por padrão**: `init_db()` só recria o banco se
  ele não existir ou se `reset=True` for passado explicitamente — evitar que
  rodar o menu normalmente apague dados já existentes.
- **Sem dependências de runtime**: `sqlite3` é módulo padrão do Python; não
  há motivo para adicionar um ORM ou driver externo a um projeto deste porte.
