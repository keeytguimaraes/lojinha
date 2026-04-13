"""
Model para operações de autenticação e gerenciamento de usuários (tabela 'login').
- id: INT PRIMARY KEY AUTO_INCREMENT
- nome: VARCHAR(100) UNIQUE - nome de usuário para login
- senha: VARCHAR(255) - senha HASHED com werkzeug.security.generate_password_hash()
- tipo_login: INT (1=ADM; 2=VENDEDOR)
"""
# Comentário geral explicando a estrutura da tabela login
# e o papel de cada campo no sistema

# Importa a conexão com o banco
from database.connection import get_db

# Importa funções de segurança para hash e verificação de senha
from werkzeug.security import generate_password_hash, check_password_hash

# Função responsável por autenticar o usuário
def login_user(nome: str, senha: str):
    """
    Autentica usuário:
    1. Busca usuário por nome
    2. Tenta validar senha com hash
    3. Fallback para senhas antigas em plain-text
    """
    
    # Cria conexão com o banco
    conn = get_db()
    
    # Cursor em formato de dicionário (melhor para acessar dados por nome)
    cursor = conn.cursor(dictionary=True)

    try:
        # Busca o usuário pelo nome
        cursor.execute("SELECT * FROM login WHERE nome = %s", (nome,))
        
        # Retorna um dicionário ou None
        user = cursor.fetchone()

        # Se não encontrou usuário, retorna None (login inválido)
        if not user:
            return None

        # Verifica senha usando hash (forma segura)
        if check_password_hash(user['senha'], senha):
            return user

        # Fallback para senhas antigas em texto puro
        # (caso existam usuários cadastrados antes do sistema de hash)
        if user['senha'] == senha:
            print("⚠️ Senha plain-text detectada.")
            return user

        # Se nenhuma validação passou, retorna None
        return None

    finally:
        # Fecha cursor e conexão (sempre executa, com erro ou não)
        cursor.close()
        conn.close()

# Função para registrar um novo login
def registrar_login(nome: str, senha: str, tipo_login: int):
    """
    Cria novo usuário no sistema (ADM ou VENDEDOR).
    - Verifica duplicado
    - Gera hash seguro da senha
    - Insere na tabela login
    """
    
    # Cria conexão com o banco
    conn = get_db()
    
    # Cursor padrão
    cursor = conn.cursor()

    try:
        # Verifica se já existe um usuário com esse nome
        cursor.execute("SELECT id FROM login WHERE nome = %s", (nome,))
        
        # Se já existir, retorna False (evita duplicidade)
        if cursor.fetchone():
            return False  # Nome já existe

        # Gera hash seguro da senha
        senha_hash = generate_password_hash(senha)

        # Insere novo usuário na tabela login
        cursor.execute(
            "INSERT INTO login (nome, senha, tipo_login) VALUES (%s, %s, %s)",
            (nome, senha_hash, tipo_login)
        )

        # Confirma a inserção no banco
        conn.commit()

        # Retorna o ID do usuário recém-criado
        return cursor.lastrowid

    finally:
        # Fecha cursor e conexão
        cursor.close()
        conn.close()