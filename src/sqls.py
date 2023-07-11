users_table_script: str = '''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY UNIQUE,
    username TEXT,
    full_name TEXT NOT NULL,
    description TEXT NOT NULL
);'''

messages_table_script: str = '''CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY UNIQUE,
    title TEXT NOT NULL,
    command TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    timestamp INTEGER NOT NULL,
    CONSTRAINT message_user_fk 
        FOREIGN KEY (user_id) REFERENCES users (id) 
            ON DELETE SET NULL
);'''

add_user_script: str = "INSERT INTO users (id, full_name, username, description) " \
                       "VALUES (?, ?, ?, ?);"

get_user_script: str = "SELECT DISTINCT id, username, full_name, description FROM users WHERE id = ?;"

add_message_script: str = "INSERT INTO messages (id, title, command, user_id, timestamp) " \
                          "VALUES (?, ?, ?, ?, ?);"

get_messages_script: str = "SELECT m.id, m.title, u.id, u.username, u.full_name FROM messages m " \
                           "INNER JOIN users u on u.id = m.user_id " \
                           "WHERE m.command = ?;"
