"""Conexão e inicialização do banco SQLite da Mini Loja."""

from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
DB_PATH = DATA_DIR / "loja.db"
SCHEMA_PATH = DATA_DIR / "schema.sql"
SEED_PATH = DATA_DIR / "seed.sql"


def get_connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    """Abre uma conexão com o banco, com chaves estrangeiras habilitadas."""
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db(db_path: Path = DB_PATH, *, reset: bool = False, seed: bool = True) -> None:
    """Cria (ou recria) o banco em `db_path` a partir de schema.sql e seed.sql.

    Se `db_path` já existir e `reset` for False, não faz nada.
    """
    if db_path.exists() and not reset:
        return

    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = get_connection(db_path)
    try:
        connection.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        if seed:
            connection.executescript(SEED_PATH.read_text(encoding="utf-8"))
        connection.commit()
    finally:
        connection.close()


def ensure_db(db_path: Path = DB_PATH) -> None:
    """Garante que o banco exista, criando-o automaticamente se necessário."""
    init_db(db_path, reset=False)


def main() -> None:
    parser = argparse.ArgumentParser(description="Gerencia o banco de dados da Mini Loja.")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Recria o banco do zero (apaga e repopula com os dados de exemplo).",
    )
    args = parser.parse_args()

    init_db(reset=args.reset)
    print(f"Banco de dados pronto em: {DB_PATH}")


if __name__ == "__main__":
    main()
