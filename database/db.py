"""
database/db.py

Database connection utilities for RealNut Intelligence.

This module provides a fresh SQLAlchemy engine whenever one
is requested. This avoids stale connections after the database
is reset.
"""

from sqlalchemy import create_engine

from config.settings import DATABASE_PATH


def get_engine():
    """
    Returns a new SQLAlchemy engine connected to the
    RealNut SQLite database.
    """

    return create_engine(
        f"sqlite:///{DATABASE_PATH}",
        echo=False,
        future=True
    )