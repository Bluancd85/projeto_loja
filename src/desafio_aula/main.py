"""Menu de terminal da Mini Loja."""

from __future__ import annotations

import sqlite3

from desafio_aula import database, queries

MENU = """
===== Mini Loja =====
1. Listar produtos (todos ou por categoria)
2. Pedidos detalhados
3. Faturamento por cliente
4. Faturamento por categoria
5. Faturamento por pedido
6. Ranking de produtos mais vendidos
0. Sair
"""


def formatar_produtos(rows: list[sqlite3.Row]) -> str:
    if not rows:
        return "Nenhum produto encontrado."
    linhas = [
        f"#{r['id']:>3} | {r['nome']:<25} | {r['categoria']:<12} | R$ {r['preco']:.2f}"
        for r in rows
    ]
    return "\n".join(linhas)


def formatar_pedidos_detalhados(rows: list[sqlite3.Row]) -> str:
    if not rows:
        return "Nenhum pedido encontrado."
    linhas = []
    pedido_atual = None
    for r in rows:
        if r["pedido_id"] != pedido_atual:
            pedido_atual = r["pedido_id"]
            linhas.append(
                f"\nPedido #{pedido_atual} | Cliente: {r['cliente_nome']} "
                f"| Data: {r['data_pedido']}"
            )
        linhas.append(
            f"  - {r['produto_nome']:<25} ({r['produto_categoria']}) "
            f"{r['quantidade']}x R$ {r['preco_unitario']:.2f} = R$ {r['subtotal']:.2f}"
        )
    return "\n".join(linhas).strip()


def formatar_faturamento_cliente(rows: list[sqlite3.Row]) -> str:
    if not rows:
        return "Nenhum faturamento encontrado."
    return "\n".join(f"{r['cliente_nome']:<25} | R$ {r['total']:.2f}" for r in rows)


def formatar_faturamento_categoria(rows: list[sqlite3.Row]) -> str:
    if not rows:
        return "Nenhum faturamento encontrado."
    return "\n".join(f"{r['categoria']:<15} | R$ {r['total']:.2f}" for r in rows)


def formatar_faturamento_pedido(rows: list[sqlite3.Row]) -> str:
    if not rows:
        return "Nenhum faturamento encontrado."
    return "\n".join(
        f"Pedido #{r['pedido_id']:<4} | {r['cliente_nome']:<25} "
        f"| {r['data_pedido']} | R$ {r['total']:.2f}"
        for r in rows
    )


def formatar_ranking(rows: list[sqlite3.Row]) -> str:
    if not rows:
        return "Nenhum produto vendido ainda."
    linhas = []
    for posicao, r in enumerate(rows, start=1):
        linhas.append(
            f"{posicao}. {r['produto_nome']:<25} | {r['quantidade_total']} unid. "
            f"| R$ {r['faturamento_total']:.2f}"
        )
    return "\n".join(linhas)


def _opcao_listar_produtos(connection: sqlite3.Connection) -> str:
    categoria = input("Filtrar por categoria (Enter para todas): ").strip()
    rows = queries.listar_produtos(connection, categoria or None)
    return formatar_produtos(rows)


def _opcao_pedidos_detalhados(connection: sqlite3.Connection) -> str:
    bruto = input("Filtrar por nº do pedido (Enter para todos): ").strip()
    if not bruto:
        return formatar_pedidos_detalhados(queries.listar_pedidos_detalhados(connection))
    try:
        pedido_id = int(bruto)
    except ValueError:
        return "Número de pedido inválido."
    return formatar_pedidos_detalhados(queries.listar_pedidos_detalhados(connection, pedido_id))


def _opcao_faturamento_cliente(connection: sqlite3.Connection) -> str:
    return formatar_faturamento_cliente(queries.faturamento_por_cliente(connection))


def _opcao_faturamento_categoria(connection: sqlite3.Connection) -> str:
    return formatar_faturamento_categoria(queries.faturamento_por_categoria(connection))


def _opcao_faturamento_pedido(connection: sqlite3.Connection) -> str:
    return formatar_faturamento_pedido(queries.faturamento_por_pedido(connection))


def _opcao_ranking(connection: sqlite3.Connection) -> str:
    return formatar_ranking(queries.ranking_produtos_mais_vendidos(connection))


OPCOES = {
    "1": _opcao_listar_produtos,
    "2": _opcao_pedidos_detalhados,
    "3": _opcao_faturamento_cliente,
    "4": _opcao_faturamento_categoria,
    "5": _opcao_faturamento_pedido,
    "6": _opcao_ranking,
}


def executar_opcao(connection: sqlite3.Connection, opcao: str) -> str | None:
    """Executa a opção de menu informada e retorna o texto de saída.

    Retorna None quando a opção é "0" (sair) e uma mensagem de erro
    quando a opção não existe.
    """
    if opcao == "0":
        return None
    handler = OPCOES.get(opcao)
    if handler is None:
        return "Opção inválida. Tente novamente."
    return handler(connection)


def main() -> None:
    database.ensure_db()
    connection = database.get_connection()
    try:
        while True:
            print(MENU)
            opcao = input("Escolha uma opção: ").strip()
            resultado = executar_opcao(connection, opcao)
            if opcao == "0":
                print("Até logo!")
                break
            print(resultado)
    finally:
        connection.close()


if __name__ == "__main__":
    main()
