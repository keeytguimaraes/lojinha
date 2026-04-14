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

# Importa funções do Flask para:
# - criar rotas (Blueprint)
# - renderizar HTML (render_template)
# - acessar dados do formulário (request)
# - redirecionar páginas (redirect, url_for)
# - exibir mensagens (flash)
# - controlar sessão do usuário (session)
from flask import Blueprint, render_template, request, redirect, url_for, flash, session

# Importa funções de login e registro do model (camada de banco de dados)
# login_user → valida usuário e senha
# registrar_login → cria novo usuário no banco
from models.login_model import login_user, registrar_login

# Importa functools para preservar metadados das funções decoradas
# (mantém nome original da função, importante para debug e Flask)
import functools

# Cria o blueprint de autenticação
# 'auth' → nome interno usado no Flask (ex: url_for('auth.login'))
# __name__ → identifica o arquivo atual
auth_bp = Blueprint('auth', __name__)


# =========================
# DECORATOR: LOGIN REQUIRED
# =========================
# Protege rotas que só podem ser acessadas por usuários logados
def login_required(f):
    
    # wraps mantém o nome original da função (boa prática)
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        
        # Verifica se existe 'user_id' na sessão
        # Se não existir, usuário não está logado
        if 'user_id' not in session:
            
            # Exibe mensagem de erro
            flash('Acesso negado! Faça login primeiro.', 'error')
            
            # Redireciona para a rota de login
            return redirect(url_for('auth.login'))
        
        # Se estiver logado, executa a função original normalmente
        return f(*args, **kwargs)
    
    # Retorna a função decorada
    return decorated_function


# =========================
# DECORATOR: ADMIN REQUIRED
# =========================
# Protege rotas exclusivas para administradores
def admin_required(f):
    
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        
        # Verifica se:
        # 1) existe 'tipo_login' na sessão
        # 2) o tipo é 1 (ADM)
        if 'tipo_login' not in session or session['tipo_login'] != 1:
            
            # Mensagem de erro
            flash('Acesso negado: somente ADM.', 'error')
            
            # Redireciona para a página inicial
            return redirect(url_for('auth.index'))
        
        # Se for ADM, executa a função normalmente
        return f(*args, **kwargs)
    
    return decorated_function


# =========================
# LOGIN
# =========================
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    
    # Verifica se o formulário foi enviado (POST)
    if request.method == 'POST':
        
        # Captura dados do formulário
        # request.form['campo'] → pega valor do input com name="campo"
        nome = request.form['nome']
        senha = request.form['senha']
        
        # Chama função que valida login no banco
        # Retorna dados do usuário se válido, ou None se inválido
        user = login_user(nome, senha)

        # Se encontrou usuário válido
        if user:
            
            # Salva informações na sessão (mantém usuário logado)
            session['user_id'] = user['id']          # ID do usuário
            session['usuario'] = user['nome']        # Nome para exibir no sistema
            session['tipo_login'] = user['tipo_login']  # 1=ADM, 2=VENDEDOR

            # Exibe mensagem de sucesso (com nome do usuário)
            flash(f'Bem-vindo, {user["nome"]}!', 'success')
            
            # Redireciona para página inicial
            return redirect(url_for('auth.index'))

        # Se login falhar (usuário ou senha incorretos)
        flash('Nome ou senha inválidos!', 'error')

    # Se for GET (acesso direto à página)
    # Apenas renderiza o formulário de login
    return render_template('login/login.html')


# =========================
# REGISTRO (APENAS ADM)
# =========================
@auth_bp.route('/registro', methods=['GET', 'POST'])
@login_required      # usuário precisa estar logado
@admin_required      # e precisa ser administrador
def registro():
    
    # Se formulário foi enviado
    if request.method == 'POST':
        
        # Captura dados do formulário
        nome = request.form['nome']
        senha = request.form['senha']
        
        # Converte tipo_login para inteiro
        # 1 = ADM | 2 = VENDEDOR
        tipo_login = int(request.form['tipo_login'])
        
        # Tenta registrar novo usuário no banco
        resultado = registrar_login(nome, senha, tipo_login)

        # Se cadastro deu certo
        if resultado:
            flash(f'Usuário {nome} criado com sucesso!', 'success')
            
            # Redireciona para home
            return redirect(url_for('auth.index'))
        
        # Se já existir usuário com mesmo nome
        else:
            flash('Nome de usuário já existe!', 'error')

    # GET → apenas exibe o formulário de registro
    return render_template('login/registro.html')


# =========================
# LOGOUT
# =========================
@auth_bp.route('/logout')
def logout():
    
    # Remove TODOS os dados da sessão
    # Isso efetivamente desloga o usuário
    session.clear()
    
    # Mensagem informando logout
    flash('Logout realizado.', 'success')
    
    # Redireciona para tela de login
    return redirect(url_for('auth.login'))


# =========================
# HOME (PÁGINA INICIAL)
# =========================
@auth_bp.route('/')
@login_required  # só usuários logados podem acessar
def index():
    
    # Renderiza a página principal do sistema
    return render_template('index.html')