"""Testes de src/desafio_aula/queries.py."""

from __future__ import annotations

import sqlite3

from desafio_aula import queries


def test_listar_produtos_sem_filtro(connection: sqlite3.Connection) -> None:
    rows = queries.listar_produtos(connection)
    assert len(rows) == 8
    nomes = [r["nome"] for r in rows]
    assert nomes == sorted(nomes)


def test_listar_produtos_com_filtro_categoria(connection: sqlite3.Connection) -> None:
    rows = queries.listar_produtos(connection, "Informática")
    assert len(rows) == 4
    assert all(r["categoria"] == "Informática" for r in rows)


def test_listar_produtos_categoria_sem_resultado(connection: sqlite3.Connection) -> None:
    rows = queries.listar_produtos(connection, "Categoria Inexistente")
    assert rows == []


def test_listar_produtos_banco_vazio(connection_vazia: sqlite3.Connection) -> None:
    rows = queries.listar_produtos(connection_vazia)
    assert rows == []


def test_listar_pedidos_detalhados_sem_filtro(connection: sqlite3.Connection) -> None:
    rows = queries.listar_pedidos_detalhados(connection)
    assert len(rows) == 13
    assert {"pedido_id", "cliente_nome", "produto_nome", "subtotal"} <= set(rows[0].keys())


def test_listar_pedidos_detalhados_com_filtro(connection: sqlite3.Connection) -> None:
    rows = queries.listar_pedidos_detalhados(connection, pedido_id=1)
    assert len(rows) == 2
    assert all(r["pedido_id"] == 1 for r in rows)


def test_listar_pedidos_detalhados_filtro_inexistente(connection: sqlite3.Connection) -> None:
    rows = queries.listar_pedidos_detalhados(connection, pedido_id=9999)
    assert rows == []


def test_faturamento_por_cliente(connection: sqlite3.Connection) -> None:
    rows = queries.faturamento_por_cliente(connection)
    assert len(rows) > 0
    totais = [r["total"] for r in rows]
    assert totais == sorted(totais, reverse=True)


def test_faturamento_por_cliente_banco_vazio(connection_vazia: sqlite3.Connection) -> None:
    rows = queries.faturamento_por_cliente(connection_vazia)
    assert rows == []


def test_faturamento_por_categoria(connection: sqlite3.Connection) -> None:
    rows = queries.faturamento_por_categoria(connection)
    categorias = {r["categoria"] for r in rows}
    assert categorias == {"Informática", "Móveis", "Áudio"}


def test_faturamento_por_pedido(connection: sqlite3.Connection) -> None:
    rows = queries.faturamento_por_pedido(connection)
    assert len(rows) == 7
    pedido_1 = next(r for r in rows if r["pedido_id"] == 1)
    assert pedido_1["total"] == 350.00 + 2 * 120.00


def test_ranking_produtos_mais_vendidos(connection: sqlite3.Connection) -> None:
    rows = queries.ranking_produtos_mais_vendidos(connection, limite=3)
    assert len(rows) == 3
    quantidades = [r["quantidade_total"] for r in rows]
    assert quantidades == sorted(quantidades, reverse=True)


def test_ranking_produtos_mais_vendidos_limite_maior_que_total(
    connection: sqlite3.Connection,
) -> None:
    rows = queries.ranking_produtos_mais_vendidos(connection, limite=1000)
    assert len(rows) <= 8


def test_ranking_produtos_mais_vendidos_banco_vazio(
    connection_vazia: sqlite3.Connection,
) -> None:
    rows = queries.ranking_produtos_mais_vendidos(connection_vazia)
    assert rows == []
