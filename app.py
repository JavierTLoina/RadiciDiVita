from flask import Flask, render_template, request, redirect, url_for, session, jsonify # Asegúrate de tener jsonify
import sqlite3
from urllib.parse import quote
import os

app = Flask(__name__)
app.secret_key = 'clave_secreta'

def validar_usuario(username, password):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE username=? AND password=?", (username, password))
    usuario = cursor.fetchone()
    conn.close()
    return usuario

@app.template_filter('url_encode')
def url_encode_filter(s):
    return quote(s)

@app.route('/')
def index():
    subject = "Richiesta di informazioni"
    body = "Buongiorno, vorrei ricevere maggiori informazioni sugli abbonamenti. Grazie"
    return render_template('index.html', subject=subject, body=body)

@app.route('/submit', methods=['POST'])
def submit():
    nombre = request.form.get('name')
    email = request.form.get('email')
    cap = request.form.get('cap')

    print(f"DEBUG: Datos recibidos del formulario - Nombre: {nombre}, Email: {email}, CAP: {cap}") # DEBUG PRINT

    if not (email and cap and nombre):
        print("DEBUG: Faltan datos requeridos en el formulario.") # DEBUG PRINT
        return "Faltan datos requeridos", 400

    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()

    try: # Añadimos un try-except para capturar errores en la DB
        cursor.execute("INSERT INTO clientes (email, cap, nombre) VALUES (?, ?, ?)", (email, cap, nombre))
        conn.commit()
        print("DEBUG: Datos insertados correctamente en la tabla clientes.") # DEBUG PRINT
    except sqlite3.Error as e:
        print(f"DEBUG: Error al insertar datos en la base de datos: {e}") # DEBUG PRINT
        conn.rollback() # Deshacer si hay error
    finally:
        conn.close()

    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['username']
        clave = request.form['password']
        if validar_usuario(usuario, clave):
            session['usuario'] = usuario
            print(f"DEBUG: Usuario {usuario} logeado correctamente.") # DEBUG PRINT
            return redirect(url_for('dashboard'))
        else:
            print(f"DEBUG: Intento de login fallido para usuario: {usuario}") # DEBUG PRINT
            return "Usuario o contraseña incorrectos", 401
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'usuario' in session:
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM clientes")
        emails_count = cursor.fetchone()[0]
        print(f"DEBUG: Total de clientes (emails_count): {emails_count}") # DEBUG PRINT

        cursor.execute("SELECT COUNT(*) FROM usuarios")
        usuarios_count = cursor.fetchone()[0]
        print(f"DEBUG: Total de usuarios: {usuarios_count}") # DEBUG PRINT


        cursor.execute("SELECT nombre, email, cap FROM clientes ORDER BY id ASC")
        clientes = cursor.fetchall()
        print(f"DEBUG: Clientes recuperados para el dashboard: {clientes}") # DEBUG PRINT

        estado_proyecto = "En lanzamiento"

        conn.close()

        return render_template(
            'dashboard.html',
            usuario=session['usuario'],
            emails_count=emails_count,
            usuarios_count=usuarios_count,
            estado_proyecto=estado_proyecto,
            clientes=clientes
        )
    print("DEBUG: Redireccionando a login, usuario no en sesión.") 
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    print("DEBUG: Sesión cerrada.") 
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
