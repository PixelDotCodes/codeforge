"""
Database Connection Module

Handles the Python <-> PostgreSQL connection layer for CodeForge.
Provides reusable connection creation and lifecycle management for future repositories.
"""

import os
from contextlib import contextmanager
import psycopg2
from psycopg2 import OperationalError, Error


class DatabaseConnectionError(Exception):
    """Raised when connecting to PostgreSQL fails."""
    pass


def get_db_config(
    host=None,
    port=None,
    dbname=None,
    user=None,
    password=None,
):
    """
    Resolve PostgreSQL connection settings.
    Prioritizes explicit arguments, then environment variables,
    and falls back to sensible local development defaults.
    """
    raw_port = port if port is not None else os.environ.get("DB_PORT", 5432)
    try:
        parsed_port = int(raw_port)
    except (ValueError, TypeError):
        parsed_port = 5432

    return {
        "host": host or os.environ.get("DB_HOST", "localhost"),
        "port": parsed_port,
        "dbname": dbname or os.environ.get("DB_NAME", "codeforge"),
        "user": user or os.environ.get("DB_USER", "postgres"),
        "password": password if password is not None else os.environ.get("DB_PASSWORD", ""),
    }


def get_connection(
    host=None,
    port=None,
    dbname=None,
    user=None,
    password=None,
    **kwargs,
):
    """
    Primary interface to obtain an active PostgreSQL connection.

    Credentials and settings are resolved from environment variables by default,
    or can be overridden with explicit arguments.
    """
    config = get_db_config(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password,
    )
    config.update(kwargs)

    try:
        return psycopg2.connect(**config)
    except (OperationalError, Error) as err:
        target = f"{config.get('user')}@{config.get('host')}:{config.get('port')}/{config.get('dbname')}"
        raise DatabaseConnectionError(
            f"Failed to connect to PostgreSQL database ({target}): {err}"
        ) from None


def close_connection(conn):
    """Safely close a database connection if open."""
    if conn is not None:
        try:
            if not getattr(conn, "closed", True):
                conn.close()
        except Exception:
            pass


@contextmanager
def get_connection_context(**kwargs):
    """
    Context manager helper for managing PostgreSQL connection lifecycle.
    Automatically closes the connection upon exiting the context block.

    Example:
        with get_connection_context() as conn:
            with conn.cursor() as cur:
                cur.execute(...)
    """
    conn = get_connection(**kwargs)
    try:
        yield conn
    finally:
        close_connection(conn)
