"""Fixtures compartilhadas: banco SQLite isolado em arquivo temporário."""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from desafio_aula import database


@pytest.fixture
def db_path(tmp_path: Path) -> Path:
    """Caminho de um banco temporário, nunca o data/loja.db real."""
    return tmp_path / "loja_teste.db"


@pytest.fixture
def connection(db_path: Path) -> sqlite3.Connection:
    """Conexão com um banco temporário já criado e populado (schema + seed)."""
    database.init_db(db_path, reset=True, seed=True)
    conn = database.get_connection(db_path)
    yield conn
    conn.close()


@pytest.fixture
def connection_vazia(db_path: Path) -> sqlite3.Connection:
    """Conexão com um banco temporário criado mas sem dados (apenas schema)."""
    database.init_db(db_path, reset=True, seed=False)
    conn = database.get_connection(db_path)
    yield conn
    conn.close()
