"""
database/init_db.py

Initializes the SQLite database.

Responsibilities
----------------
- Delete the existing database
- Create a fresh empty SQLite database
"""

from pathlib import Path

from config.settings import DATABASE_PATH
from database.db import get_engine


class DatabaseInitializer:

    def __init__(self):
        self.database_path = Path(DATABASE_PATH)

    def reset_database(self):
        """
        Deletes the existing database and creates
        a new empty SQLite database.
        """

        if self.database_path.exists():
            self.database_path.unlink()

        engine = get_engine()

        # Create an empty SQLite database
        with engine.begin():
            pass

        engine.dispose()

    def database_exists(self):

        return self.database_path.exists()