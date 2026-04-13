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
 Múltiplos ADMs: Risco se não limitar criação manual.

FLASH: Mensagens temporárias (sucesso/erro).
"""
# Comentário geral explicando o funcionamento das rotas de autenticação,
# controle de acesso e uso de sessões

# Importa funções do Flask para rotas, templates, requisições e sessão
from flask import Blueprint, render_template, request, redirect, url_for, flash, session

# Importa funções de login e registro do model
from models.login_model import login_user, registrar_login

# Importa functools para preservar metadados nas funções decoradas
import functools

# Cria o blueprint de autenticação
auth_bp = Blueprint('auth', __name__)


#  Decorator para proteger rotas que exigem login
def login_required(f):
    @functools.wraps(f)  # mantém nome e propriedades da função original
    def decorated_function(*args, **kwargs):
        
        # Verifica se o usuário está logado (session contém user_id)
        if 'user_id' not in session:
            
            # Mensagem de erro
            flash('Acesso negado! Faça login primeiro.', 'error')
            
            # Redireciona para a página de login
            return redirect(url_for('auth.login'))
        
        # Se estiver logado, executa a função normalmente
        return f(*args, **kwargs)
    
    return decorated_function


#  Decorator para rotas só para ADM
def admin_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        
        # Verifica se é ADM (tipo_login == 1)
        if 'tipo_login' not in session or session['tipo_login'] != 1:
            
            # Mensagem de erro
            flash('Acesso negado: somente ADM.', 'error')
            
            # Redireciona para a página inicial
            return redirect(url_for('auth.index'))
        
        return f(*args, **kwargs)
    
    return decorated_function


#  LOGIN
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    
    # Se o formulário foi enviado
    if request.method == 'POST':
        
        # Pega dados do formulário
        nome = request.form['nome']
        senha = request.form['senha']
        
        # Tenta autenticar usuário
        user = login_user(nome, senha)

        # Se login válido
        if user:
            
            # Salva dados na sessão (usuário fica "logado")
            session['user_id'] = user['id']
            session['usuario'] = user['nome']   # nome usado no sistema/frontend
            session['tipo_login'] = user['tipo_login']

            # Mensagem de boas-vindas
            flash(f'Bem-vindo, {user["nome"]}!', 'success')
            
            # Redireciona para a página inicial
            return redirect(url_for('auth.index'))

        # Caso login falhe
        flash('Nome ou senha inválidos!', 'error')

    # GET → exibe formulário de login
    return render_template('login/login.html')


#  REGISTRO (somente ADM)
@auth_bp.route('/registro', methods=['GET', 'POST'])
@login_required      # precisa estar logado
@admin_required      # e precisa ser ADM
def registro():
    
    if request.method == 'POST':
        
        # Pega dados do formulário
        nome = request.form['nome']
        senha = request.form['senha']
        tipo_login = int(request.form['tipo_login'])  # 1=ADM, 2=VENDEDOR
        
        # Tenta registrar novo usuário
        resultado = registrar_login(nome, senha, tipo_login)

        # Se deu certo
        if resultado:
            flash(f'Usuário {nome} criado com sucesso!', 'success')
            return redirect(url_for('auth.index'))
        
        # Se já existe
        else:
            flash('Nome de usuário já existe!', 'error')

    # GET → exibe formulário
    return render_template('login/registro.html')


#  LOGOUT
@auth_bp.route('/logout')
def logout():
    
    # Limpa toda a sessão (desloga usuário)
    session.clear()
    
    # Mensagem de confirmação
    flash('Logout realizado.', 'success')
    
    # Redireciona para login
    return redirect(url_for('auth.login'))


#  HOME
@auth_bp.route('/')
@login_required
def index():
    
    # Página inicial do sistema (apenas usuários logados)
    return render_template('index.html')