import sqlite3

conn = sqlite3.connect('usuarios.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL,
        cap TEXT NOT NULL
    )
''')

try:
    cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", ('admin', 'admin123'))
    conn.commit()
    print("Usuario 'admin' creado con contraseña 'admin123'.")
except sqlite3.IntegrityError:
    print("Usuario 'admin' ya existe.")

conn.close()

