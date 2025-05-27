from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'clave_secreta'

def validar_usuario(username, password):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE username=? AND password=?", (username, password))
    usuario = cursor.fetchone()
    conn.close()
    return usuario

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
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM clientes")
        emails_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        usuarios_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT email, cap FROM clientes")
        clientes = cursor.fetchall()
        
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
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
