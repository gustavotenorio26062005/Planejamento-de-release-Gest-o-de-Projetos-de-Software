from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import hashlib
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'uma_chave_secreta_muito_segura' # Necessário para usar sessões e mensagens flash

# Funções de banco de dados
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    conn.commit()
    conn.close()

# Inserir um usuário admin padrão se não existir
def insert_admin():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = 'admin'")
    admin = cursor.fetchone()
    if not admin:
        password_hash = hashlib.sha256('admin123'.encode()).hexdigest()
        conn.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                     ('admin', password_hash, 'admin'))
        conn.commit()
    conn.close()

# Rota de login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ? AND password = ?",
                            (username, password_hash)).fetchone()
        conn.close()

        if user:
            session['logged_in'] = True
            session['username'] = user['username']
            session['role'] = user['role']
            flash(f"Bem-vindo, {user['username']}!", 'success')
            return redirect(url_for('dashboard'))
        else:
            flash("Usuário ou senha inválidos.", 'danger')

    return render_template('index.html')

# Rota de cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        role = request.form['role']
        
        conn = get_db_connection()
        try:
            conn.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                         (username, password_hash, role))
            conn.commit()
            flash("Cadastro realizado com sucesso! Faça login para continuar.", 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Este nome de usuário já existe.", 'danger')
        finally:
            conn.close()

    return render_template('cadastro.html')

# Rota do painel (dashboard)
@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    return render_template('dashboard.html')

# Rota de gerenciamento de usuários (apenas para admin)
@app.route('/users')
def users_management():
    if 'role' not in session or session['role'] != 'admin':
        flash("Acesso negado. Você não tem permissão para acessar esta página.", 'warning')
        return redirect(url_for('dashboard'))

    conn = get_db_connection()
    users = conn.execute("SELECT id, username, role, created_at FROM users").fetchall()
    conn.close()

    return render_template('users.html', users=users)

# Rota para editar usuário (admin)
@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    # Verificação de permissão (apenas admin)
    if 'role' not in session or session['role'] != 'admin':
        flash("Acesso negado.", 'warning')
        return redirect(url_for('dashboard'))

    conn = get_db_connection()
    user = conn.execute("SELECT id, username, role FROM users WHERE id = ?", (user_id,)).fetchone()
    
    if request.method == 'POST':
        new_username = request.form['username']
        new_role = request.form['role']
        conn.execute("UPDATE users SET username = ?, role = ? WHERE id = ?",
                     (new_username, new_role, user_id))
        conn.commit()
        conn.close()
        flash("Usuário atualizado com sucesso.", 'success')
        return redirect(url_for('users_management'))

    conn.close()
    return render_template('edit_user.html', user=user)

# Rota para excluir usuário (admin)
@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if 'role' not in session or session['role'] != 'admin':
        flash("Acesso negado.", 'warning')
        return redirect(url_for('dashboard'))
    
    conn = get_db_connection()
    conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    flash("Usuário excluído com sucesso.", 'success')
    return redirect(url_for('users_management'))


# Rota de logout
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('role', None)
    flash("Você foi desconectado.", 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    create_table()
    insert_admin()
    app.run(debug=True)