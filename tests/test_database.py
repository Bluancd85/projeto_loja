"""Testes de src/desafio_aula/database.py."""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from desafio_aula import database


def test_get_connection_configura_row_factory_e_fk(db_path: Path) -> None:
    database.init_db(db_path, reset=True)
    conn = database.get_connection(db_path)
    try:
        fk_status = conn.execute("PRAGMA foreign_keys").fetchone()[0]
        assert fk_status == 1
        row = conn.execute("SELECT 1 AS valor").fetchone()
        assert isinstance(row, sqlite3.Row)
        assert row["valor"] == 1
    finally:
        conn.close()


def test_init_db_cria_arquivo_e_tabelas(db_path: Path) -> None:
    assert not db_path.exists()
    database.init_db(db_path, reset=True)
    assert db_path.exists()

    conn = database.get_connection(db_path)
    try:
        tabelas = {
            row["name"]
            for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            ).fetchall()
        }
    finally:
        conn.close()
    assert {"clientes", "produtos", "pedidos", "itens_pedido"} <= tabelas


def test_init_db_popula_dados_de_exemplo(connection: sqlite3.Connection) -> None:
    total_clientes = connection.execute("SELECT COUNT(*) FROM clientes").fetchone()[0]
    total_produtos = connection.execute("SELECT COUNT(*) FROM produtos").fetchone()[0]
    assert total_clientes > 0
    assert total_produtos > 0


def test_init_db_sem_seed_nao_popula(connection_vazia: sqlite3.Connection) -> None:
    total_clientes = connection_vazia.execute("SELECT COUNT(*) FROM clientes").fetchone()[0]
    assert total_clientes == 0


def test_init_db_sem_reset_preserva_banco_existente(db_path: Path) -> None:
    database.init_db(db_path, reset=True)
    conn = database.get_connection(db_path)
    conn.execute("INSERT INTO clientes (nome, email, cidade) VALUES ('X', 'x@x.com', 'X')")
    conn.commit()
    conn.close()

    database.init_db(db_path, reset=False)

    conn = database.get_connection(db_path)
    try:
        total = conn.execute("SELECT COUNT(*) FROM clientes WHERE nome = 'X'").fetchone()[0]
    finally:
        conn.close()
    assert total == 1


def test_init_db_com_reset_recria_banco(db_path: Path) -> None:
    database.init_db(db_path, reset=True)
    conn = database.get_connection(db_path)
    conn.execute("INSERT INTO clientes (nome, email, cidade) VALUES ('X', 'x@x.com', 'X')")
    conn.commit()
    conn.close()

    database.init_db(db_path, reset=True)

    conn = database.get_connection(db_path)
    try:
        total = conn.execute("SELECT COUNT(*) FROM clientes WHERE nome = 'X'").fetchone()[0]
    finally:
        conn.close()
    assert total == 0


def test_ensure_db_cria_quando_nao_existe(db_path: Path) -> None:
    assert not db_path.exists()
    database.ensure_db(db_path)
    assert db_path.exists()


def test_main_cli_reset(monkeypatch: pytest.MonkeyPatch, db_path: Path) -> None:
    chamadas: list[bool] = []

    def fake_init_db(*, reset: bool = False) -> None:
        chamadas.append(reset)

    monkeypatch.setattr(database, "init_db", fake_init_db)
    monkeypatch.setattr("sys.argv", ["database.py", "--reset"])

    database.main()

    assert chamadas == [True]


def test_main_cli_sem_reset(monkeypatch: pytest.MonkeyPatch) -> None:
    chamadas: list[bool] = []

    def fake_init_db(*, reset: bool = False) -> None:
        chamadas.append(reset)

    monkeypatch.setattr(database, "init_db", fake_init_db)
    monkeypatch.setattr("sys.argv", ["database.py"])

    database.main()

    assert chamadas == [False]
