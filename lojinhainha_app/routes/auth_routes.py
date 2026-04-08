"""
Rotas de autenticação (Blueprint padrão sem prefix).
- /login (GET: form; POST: auth)
- /registro (GET/POST: apenas ADM cria contas)
- /logout

DECORATORS (Segurança via sessões Flask):
- @login_required: Verifica session['user_id']. Redireciona para /login se não logado.
  - session gerenciada por Flask (cookies seguros).
- @admin_required: session['tipo_login'] == 1. ADM vê tudo; Vendedor limitado.

SESSÃO: Após login, armazena {'user_id': id, 'nome': nome, 'tipo_login': 1|2}
⚠️ Múltiplos ADMs: Risco se não limitar criação manual.

FLASH: Mensagens temporárias (sucesso/erro).
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.login_model import login_user, registrar_login
import functools

auth_bp = Blueprint('auth', __name__)

# 🔹 Decorator para proteger rotas que exigem login
def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Acesso negado! Faça login primeiro.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

# 🔹 Decorator para rotas só para ADM
def admin_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if 'tipo_login' not in session or session['tipo_login'] != 1:
            flash('Acesso negado: somente ADM.', 'error')
            return redirect(url_for('auth.index'))
        return f(*args, **kwargs)
    return decorated_function

# 🔹 LOGIN
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        user = login_user(nome, senha)

        if user:
            # ✅ PADRONIZAÇÃO AQUI (IMPORTANTE)
            session['user_id'] = user['id']
            session['usuario'] = user['nome']   # 🔥 AGORA BATE COM O HTML
            session['tipo_login'] = user['tipo_login']

            flash(f'Bem-vindo, {user["nome"]}!', 'success')
            return redirect(url_for('auth.index'))

        flash('Nome ou senha inválidos!', 'error')

    return render_template('login/login.html')


# 🔹 REGISTRO (ADM)
@auth_bp.route('/registro', methods=['GET', 'POST'])
@login_required
@admin_required
def registro():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        tipo_login = int(request.form['tipo_login'])
        
        resultado = registrar_login(nome, senha, tipo_login)

        if resultado:
            flash(f'Usuário {nome} criado com sucesso!', 'success')
            return redirect(url_for('auth.index'))
        else:
            flash('Nome de usuário já existe!', 'error')

    return render_template('login/registro.html')


# 🔹 LOGOUT
@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Logout realizado.', 'success')
    return redirect(url_for('auth.login'))


# 🔹 HOME
@auth_bp.route('/')
@login_required
def index():
    return render_template('index.html')