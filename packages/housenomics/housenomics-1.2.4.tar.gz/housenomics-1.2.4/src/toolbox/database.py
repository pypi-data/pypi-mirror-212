import os
import pathlib
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy import text as _text
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session as _Session

Session = _Session
text = _text


class Base(DeclarativeBase):
    pass


class Database:
    """
    Creates a database in the path defined by the DATABASE environment variable.
    If the environment variable is not defined, it will create a database in the
    path defined by the database_path parameter.

    Optionally, it can receive a SQL file that will be executed against the database.
    """

    def __init__(
        self,
        database_path: Optional[pathlib.Path] = None,
        sql_file: Optional[pathlib.Path] = None,
    ) -> None:
        """
        param: database_name: Path to where the database file will be created.
        param: sql_file: Path to the SQL file that will be executed against the database.
        """

        # Get the database path from the environment variable
        # The environment variable always has priority over the definition
        # defined by the application.
        env_path = os.environ.get("DATABASE")
        if env_path:
            database_path = pathlib.Path(env_path)

        # Create the database file location
        if not database_path:
            raise KeyError("Please set the DATABASE environment variable.")
        database_path.mkdir(parents=True, exist_ok=True)
        self._database_file = database_path / "database.db"
        sqlite_url = f"sqlite:///{self._database_file}"

        # Create the database engine
        engine = create_engine(sqlite_url, echo=False)
        self.engine = engine

        # Create the database tables
        if sql_file:
            with Session(engine) as session:
                _run_sql_file(pathlib.Path(sql_file), session)

    def remove(self):
        """
        Removes the database file from the disk if it exists.
        """
        pathlib.Path(self._database_file).unlink(missing_ok=True)


def _run_sql_file(sql_file_path: pathlib.Path, session):
    """
    Runs the SQL in sql_file_path against the database.
    """

    with open(sql_file_path) as sql_file:
        sql = sql_file.read()
        session.execute(text(sql))
