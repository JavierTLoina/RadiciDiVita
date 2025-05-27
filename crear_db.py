import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect('usuarios.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')

hashed_password = generate_password_hash('admin123')
try:
    cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", ('admin', hashed_password))
    print("Usuario 'admin' creado con contraseña hasheada.")
except sqlite3.IntegrityError:
    print("El usuario 'admin' ya existe. No se agregó de nuevo.")

conn.commit()
conn.close()
print("Base de datos creada o actualizada.")
