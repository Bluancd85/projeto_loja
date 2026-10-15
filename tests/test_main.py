"""Testes de src/desafio_aula/main.py."""

from __future__ import annotations

import sqlite3

import pytest

from desafio_aula import database, main, queries


def test_formatar_produtos_vazio() -> None:
    assert main.formatar_produtos([]) == "Nenhum produto encontrado."


def test_formatar_produtos_com_dados(connection: sqlite3.Connection) -> None:
    rows = queries.listar_produtos(connection)
    texto = main.formatar_produtos(rows)
    assert "Teclado Mecânico" in texto


def test_formatar_pedidos_detalhados_vazio() -> None:
    assert main.formatar_pedidos_detalhados([]) == "Nenhum pedido encontrado."


def test_formatar_pedidos_detalhados_agrupa_por_pedido(connection: sqlite3.Connection) -> None:
    rows = queries.listar_pedidos_detalhados(connection)
    texto = main.formatar_pedidos_detalhados(rows)
    assert "Pedido #1" in texto
    assert "Cliente:" in texto


def test_formatar_faturamento_cliente_vazio() -> None:
    assert main.formatar_faturamento_cliente([]) == "Nenhum faturamento encontrado."


def test_formatar_faturamento_cliente_com_dados(connection: sqlite3.Connection) -> None:
    rows = queries.faturamento_por_cliente(connection)
    texto = main.formatar_faturamento_cliente(rows)
    assert "R$" in texto


def test_formatar_faturamento_categoria_vazio() -> None:
    assert main.formatar_faturamento_categoria([]) == "Nenhum faturamento encontrado."


def test_formatar_faturamento_categoria_com_dados(connection: sqlite3.Connection) -> None:
    rows = queries.faturamento_por_categoria(connection)
    texto = main.formatar_faturamento_categoria(rows)
    assert "Informática" in texto


def test_formatar_faturamento_pedido_vazio() -> None:
    assert main.formatar_faturamento_pedido([]) == "Nenhum faturamento encontrado."


def test_formatar_faturamento_pedido_com_dados(connection: sqlite3.Connection) -> None:
    rows = queries.faturamento_por_pedido(connection)
    texto = main.formatar_faturamento_pedido(rows)
    assert "Pedido #1" in texto


def test_formatar_ranking_vazio() -> None:
    assert main.formatar_ranking([]) == "Nenhum produto vendido ainda."


def test_formatar_ranking_com_dados(connection: sqlite3.Connection) -> None:
    rows = queries.ranking_produtos_mais_vendidos(connection)
    texto = main.formatar_ranking(rows)
    assert texto.startswith("1.")


def test_opcao_listar_produtos_sem_filtro(
    monkeypatch: pytest.MonkeyPatch, connection: sqlite3.Connection
) -> None:
    monkeypatch.setattr("builtins.input", lambda *_: "")
    texto = main._opcao_listar_produtos(connection)
    assert "Teclado Mecânico" in texto


def test_opcao_listar_produtos_com_filtro(
    monkeypatch: pytest.MonkeyPatch, connection: sqlite3.Connection
) -> None:
    monkeypatch.setattr("builtins.input", lambda *_: "Móveis")
    texto = main._opcao_listar_produtos(connection)
    assert "Cadeira Gamer" in texto
    assert "Teclado" not in texto


def test_opcao_pedidos_detalhados_sem_filtro(
    monkeypatch: pytest.MonkeyPatch, connection: sqlite3.Connection
) -> None:
    monkeypatch.setattr("builtins.input", lambda *_: "")
    texto = main._opcao_pedidos_detalhados(connection)
    assert "Pedido #1" in texto


def test_opcao_pedidos_detalhados_com_filtro_valido(
    monkeypatch: pytest.MonkeyPatch, connection: sqlite3.Connection
) -> None:
    monkeypatch.setattr("builtins.input", lambda *_: "1")
    texto = main._opcao_pedidos_detalhados(connection)
    assert "Pedido #1" in texto
    assert "Pedido #2" not in texto


def test_opcao_pedidos_detalhados_com_filtro_invalido(
    monkeypatch: pytest.MonkeyPatch, connection: sqlite3.Connection
) -> None:
    monkeypatch.setattr("builtins.input", lambda *_: "abc")
    texto = main._opcao_pedidos_detalhados(connection)
    assert texto == "Número de pedido inválido."


def test_executar_opcao_sair_retorna_none(connection: sqlite3.Connection) -> None:
    assert main.executar_opcao(connection, "0") is None


def test_executar_opcao_invalida(connection: sqlite3.Connection) -> None:
    assert main.executar_opcao(connection, "99") == "Opção inválida. Tente novamente."


def test_executar_opcao_faturamento_cliente(connection: sqlite3.Connection) -> None:
    texto = main.executar_opcao(connection, "3")
    assert "R$" in texto


def test_main_loop_percorre_menu_e_sai(
    monkeypatch: pytest.MonkeyPatch,
    connection: sqlite3.Connection,
    capsys: pytest.CaptureFixture[str],
) -> None:
    entradas = iter(["1", "", "2", "", "3", "4", "5", "6", "99", "0"])
    monkeypatch.setattr("builtins.input", lambda *_: next(entradas))
    monkeypatch.setattr(database, "ensure_db", lambda: None)
    monkeypatch.setattr(database, "get_connection", lambda: connection)

    main.main()

    saida = capsys.readouterr().out
    assert "Até logo!" in saida
    assert "Opção inválida" in saida
