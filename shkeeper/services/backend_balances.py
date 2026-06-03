import os
from dataclasses import dataclass
from decimal import Decimal
from functools import lru_cache

from flask import current_app
from sqlalchemy import create_engine, text


@dataclass(frozen=True)
class BackendBalance:
    amount: Decimal | None
    configured: bool
    error: str | None = None


@lru_cache(maxsize=8)
def _engine(database_uri: str):
    return create_engine(
        database_uri,
        pool_pre_ping=True,
        pool_recycle=int(os.environ.get("BALANCE_DB_POOL_RECYCLE", "300")),
        pool_size=int(os.environ.get("BALANCE_DB_POOL_SIZE", "2")),
        max_overflow=int(os.environ.get("BALANCE_DB_MAX_OVERFLOW", "4")),
        pool_timeout=int(os.environ.get("BALANCE_DB_POOL_TIMEOUT", "5")),
    )


def _scalar_decimal(database_uri: str | None, sql: str, params: dict) -> BackendBalance:
    if not database_uri:
        return BackendBalance(amount=None, configured=False)
    try:
        with _engine(database_uri).connect() as conn:
            value = conn.execute(text(sql), params).scalar()
    except Exception as exc:
        current_app.logger.warning("Backend balance query failed: %s", exc)
        return BackendBalance(amount=None, configured=True, error=str(exc))
    if value is None:
        return BackendBalance(amount=Decimal("0"), configured=True)
    return BackendBalance(amount=Decimal(str(value)), configured=True)


def evm_accounts_balance(network_symbol: str, crypto: str) -> BackendBalance:
    database_uri = (
        os.environ.get(f"{network_symbol}_BALANCES_DATABASE_URI")
        or os.environ.get("EVM_BALANCES_DATABASE_URI")
    )
    return _scalar_decimal(
        database_uri,
        """
        SELECT COALESCE(SUM(amount), 0)
        FROM accounts
        WHERE crypto = :crypto
        """,
        {"crypto": crypto},
    )


def tron_accounts_balance(crypto: str) -> BackendBalance:
    database_uri = os.environ.get("TRON_BALANCES_DATABASE_URI")
    return _scalar_decimal(
        database_uri,
        """
        SELECT COALESCE(SUM(balance), 0)
        FROM tron_balances
        WHERE symbol = :crypto
        """,
        {"crypto": crypto},
    )
