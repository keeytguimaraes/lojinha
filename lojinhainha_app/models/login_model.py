"""
Model para operações de autenticação e gerenciamento de usuários (tabela 'login').
- id: INT PRIMARY KEY AUTO_INCREMENT
- nome: VARCHAR(100) UNIQUE - nome de usuário para login
- senha: VARCHAR(255) - senha HASHED com werkzeug.security.generate_password_hash()
- tipo_login: INT (1=ADM; 2=VENDEDOR)
"""

from database.connection import get_db
from werkzeug.security import generate_password_hash, check_password_hash

def login_user(nome: str, senha: str):
    """
    Autentica usuário:
    1. Busca usuário por nome
    2. Tenta validar senha com hash
    3. Fallback para senhas antigas em plain-text
    """
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM login WHERE nome = %s", (nome,))
        user = cursor.fetchone()
        if not user:
            return None
        # Verifica hash
        if check_password_hash(user['senha'], senha):
            return user
        # Fallback plain-text
        if user['senha'] == senha:
            print("⚠️ Senha plain-text detectada.")
            return user
        return None
    finally:
        cursor.close()
        conn.close()

def registrar_login(nome: str, senha: str, tipo_login: int):
    """
    Cria novo usuário no sistema (ADM ou VENDEDOR).
    - Verifica duplicado
    - Gera hash seguro da senha
    - Insere na tabela login
    """
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM login WHERE nome = %s", (nome,))
        if cursor.fetchone():
            return False  # Nome já existe
        senha_hash = generate_password_hash(senha)
        cursor.execute(
            "INSERT INTO login (nome, senha, tipo_login) VALUES (%s, %s, %s)",
            (nome, senha_hash, tipo_login)
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        cursor.close()
        conn.close()