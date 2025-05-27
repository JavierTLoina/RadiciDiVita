from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import check_password_hash  

app = Flask(__name__)
app.secret_key = 'clave_secreta'

def validar_usuario(username, password):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE username=?", (username,))
    usuario = cursor.fetchone()
    conn.close()
    
    if usuario:
        if check_password_hash(usuario[2], password):
            return usuario
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['username']
        clave = request.form['password']
        if validar_usuario(usuario, clave):
            session['usuario'] = usuario
            return redirect(url_for('dashboard'))
        else:
            return "Usuario o contraseña incorrectos", 401
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'usuario' in session:
        return render_template('dashboard.html', usuario=session['usuario'])
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
