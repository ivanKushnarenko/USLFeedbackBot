from  contextlib import contextmanager
import logging as log
import sqlite3 as sql
from typing import Optional

import config
import sqls as scripts
from user import User


def _logger():
    logger = log.getLogger(__name__)
    logger.setLevel(log.INFO)
    return logger


@contextmanager
def _init_connection():
    connection = sql.connect(config.DB_FILE)
    try:
        yield connection
    except sql.Error as e:
        _logger().error(f'Error during connection initialization: {str(e)}')
    finally:
        connection.close()


def _ensure_tables():
    with _init_connection() as conn:
        with conn:
            conn.execute(scripts.users_table_script)
            conn.execute(scripts.messages_script)


def add_user(user: User):
    with _init_connection() as conn:
        query: str = "INSERT INTO users (id, full_name, username, description) " \
                     "VALUES (?, ?, ?, ?);"
        params: tuple = (user.id, user.full_name, user.username, user.description)

        with conn:
            conn.execute(query, params)


def get_user(user_id: int) -> Optional[User]:
    with _init_connection() as conn:
        query = "SELECT (id, username, full_name, description) FROM users WHERE id = ?;"
        with conn:
            conn.execute(query, (user_id,))
            if (fetch_result := conn.fetchone()) is not None:
                user_id, name, full_name, descr = fetch_result
                return User(id=user_id, username=name, full_name=full_name, description=descr)
            return None


def add_message(message_id: int, user_id, user):
    pass


# ensure that all necessary tables are created in database
_ensure_tables()
