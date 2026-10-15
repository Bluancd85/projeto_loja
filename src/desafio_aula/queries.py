"""Consultas SQL dos relatórios da Mini Loja."""

from __future__ import annotations

import sqlite3


def listar_produtos(
    connection: sqlite3.Connection, categoria: str | None = None
) -> list[sqlite3.Row]:
    """Lista produtos, opcionalmente filtrados por categoria."""
    if categoria is None:
        cursor = connection.execute("SELECT id, nome, categoria, preco FROM produtos ORDER BY nome")
    else:
        cursor = connection.execute(
            """
            SELECT id, nome, categoria, preco
            FROM produtos
            WHERE categoria = ?
            ORDER BY nome
            """,
            (categoria,),
        )
    return cursor.fetchall()


def listar_pedidos_detalhados(
    connection: sqlite3.Connection, pedido_id: int | None = None
) -> list[sqlite3.Row]:
    """Lista itens de pedidos com dados de cliente e produto (via JOIN).

    Cada linha representa um item de pedido; linhas do mesmo pedido
    compartilham `pedido_id`, `cliente_nome` e `data_pedido`.
    """
    if pedido_id is None:
        cursor = connection.execute(
            """
            SELECT pedido_id, data_pedido, cliente_nome,
                   produto_nome, produto_categoria,
                   quantidade, preco_unitario, subtotal
            FROM vw_itens_detalhados
            ORDER BY pedido_id, produto_nome
            """
        )
    else:
        cursor = connection.execute(
            """
            SELECT pedido_id, data_pedido, cliente_nome,
                   produto_nome, produto_categoria,
                   quantidade, preco_unitario, subtotal
            FROM vw_itens_detalhados
            WHERE pedido_id = ?
            ORDER BY produto_nome
            """,
            (pedido_id,),
        )
    return cursor.fetchall()


def faturamento_por_cliente(connection: sqlite3.Connection) -> list[sqlite3.Row]:
    """Soma o faturamento (quantidade x preço) agrupado por cliente."""
    cursor = connection.execute(
        """
        SELECT cliente_nome, SUM(subtotal) AS total
        FROM vw_itens_detalhados
        GROUP BY cliente_id, cliente_nome
        ORDER BY total DESC
        """
    )
    return cursor.fetchall()


def faturamento_por_categoria(connection: sqlite3.Connection) -> list[sqlite3.Row]:
    """Soma o faturamento agrupado por categoria de produto."""
    cursor = connection.execute(
        """
        SELECT produto_categoria AS categoria, SUM(subtotal) AS total
        FROM vw_itens_detalhados
        GROUP BY produto_categoria
        ORDER BY total DESC
        """
    )
    return cursor.fetchall()


def faturamento_por_pedido(connection: sqlite3.Connection) -> list[sqlite3.Row]:
    """Soma o faturamento agrupado por pedido."""
    cursor = connection.execute(
        """
        SELECT pedido_id, cliente_nome, data_pedido, SUM(subtotal) AS total
        FROM vw_itens_detalhados
        GROUP BY pedido_id, cliente_nome, data_pedido
        ORDER BY pedido_id
        """
    )
    return cursor.fetchall()


def ranking_produtos_mais_vendidos(
    connection: sqlite3.Connection, limite: int = 5
) -> list[sqlite3.Row]:
    """Rankeia produtos por quantidade total vendida (desc)."""
    cursor = connection.execute(
        """
        SELECT produto_nome, SUM(quantidade) AS quantidade_total,
               SUM(subtotal) AS faturamento_total
        FROM vw_itens_detalhados
        GROUP BY produto_id, produto_nome
        ORDER BY quantidade_total DESC, faturamento_total DESC
        LIMIT ?
        """,
        (limite,),
    )
    return cursor.fetchall()
