from  contextlib import contextmanager
import logging as log
import sqlite3 as sql
from typing import Optional
import datetime as dt

import config
import sqls as scripts
from user import User
from commands import CommandType, as_command_text


def _logger():
    logger = log.getLogger(__name__)
    logger.setLevel(log.INFO)
    return logger


@contextmanager
def _db_connection():
    connection = None
    try:
        connection = sql.connect(config.DB_FILE)
        yield connection
    except sql.Error as e:
        _logger().error(f'Error during connection initialization: {str(e)}')
    finally:
        connection.close()


def _ensure_tables():
    with _db_connection() as conn:
        with conn:
            conn.execute(scripts.users_table_script)
            conn.execute(scripts.messages_table_script)


def add_user(user: User):
    with _db_connection() as conn:
        with conn:
            query: str = "INSERT INTO users (id, full_name, username, description) " \
                         "VALUES (?, ?, ?, ?);"
            params: tuple = (user.id, user.full_name, user.username, user.description)
            conn.execute(query, params)


def get_user(user_id: int) -> Optional[User]:
    with _db_connection() as conn:
        cur: sql.Cursor = conn.cursor()
        cur.execute(scripts.get_user_script, (user_id,))
        if (fetch_result := cur.fetchone()) is not None:
            user_id, name, full_name, descr = fetch_result
            return User(id=user_id, username=name, full_name=full_name, description=descr)
        return None


def add_message(message_id: int, title: str, cmd: CommandType, user_id: int):
    with _db_connection() as conn:
        with conn:
            params: tuple = (message_id, title, as_command_text(cmd), user_id,
                             int(dt.datetime.now().strftime("%Y%m%d%H%M%S")))
            conn.execute(scripts.add_message_script, params)


def get_messages(cmd: CommandType):
    pass


# ensure that all necessary tables are created in database
_ensure_tables()
