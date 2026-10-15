# Uso

## Criar/popular o banco de dados

O banco é criado automaticamente na primeira execução do menu, mas também
pode ser (re)criado manualmente:

```bash
# Cria o banco só se ele ainda não existir
poetry run python -m desafio_aula.database

# Apaga e recria o banco do zero, repopulando com os dados de exemplo
poetry run python -m desafio_aula.database --reset
```

O banco fica em `data/loja.db` (não é versionado — veja `.gitignore`). O
schema e os dados de exemplo vêm de `data/schema.sql` e `data/seed.sql`.

## Rodar o menu

```bash
poetry run python -m desafio_aula.main
```

Como bônus, também há um script instalado pelo Poetry:

```bash
poetry run desafio-aula
```

## Relatórios disponíveis no menu

1. **Listar produtos** — lista todos os produtos ou filtra por categoria
   (basta digitar o nome da categoria ou pressionar Enter para listar todos).
2. **Pedidos detalhados** — lista os itens de cada pedido, juntando dados de
   cliente, pedido e produto; pode ser filtrado por número do pedido.
3. **Faturamento por cliente** — soma o valor total comprado por cada cliente.
4. **Faturamento por categoria** — soma o valor total vendido por categoria
   de produto.
5. **Faturamento por pedido** — soma o valor total de cada pedido individual.
6. **Ranking de produtos mais vendidos** — ordena os produtos pela quantidade
   total vendida.
0. **Sair** — encerra a aplicação.
