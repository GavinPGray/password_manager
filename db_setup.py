import sqlite3


def create_db():
    conn = sqlite3.connect('password_manager.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
    (id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    hashed_password TEXT,
    salt TEXT,
    encrypted_key TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS passwords
    (id INTEGER PRIMARY KEY,
    user_id INTEGER,
    website TEXT,
    username TEXT,
    encrypted_password TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id))''')
    print('Database created successfully')
    input('Press Enter to continue...')
    conn.commit()
    conn.close()


def delete_user():
    conn = sqlite3.connect('password_manager.db')
    cursor = conn.cursor()
    cursor.execute('Delete from passwords where id = 5')
    print('User deleted successfully')
    input('Press Enter to continue...')
    conn.commit()
    conn.close()


