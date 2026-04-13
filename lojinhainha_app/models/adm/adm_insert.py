# Importa a função get_db responsável por criar a conexão com o banco de dados
from database.connection import get_db

# Importação comentada (não está sendo usada)
# Antes, provavelmente essa função era chamada aqui para registrar login
# Agora o fluxo foi alterado (login é criado antes e só o login_id é passado)
# from models.login_model import registrar_login  # Removed

# Define a função inserir_adm, que recebe os dados do administrador
# incluindo o login_id já criado previamente
def inserir_adm(nome, cpf, email, data_nascimento, login_id):
    
    """
     FIX: Updated to use pre-registered login_id.
    - Indica que houve uma correção no código
    - Agora o login_id não é criado aqui, mas recebido como parâmetro

    - Matches pattern of vendedor_insert.
    - O padrão de inserção agora segue o mesmo usado para vendedores

    - Routes should call registrar_login first, then this.
    - As rotas devem primeiro criar o login (com senha e hash),
      depois chamar essa função para inserir o ADM

    Note: adm_routes.py currently passes 4 args — needs route fix if used.
    - Aqui há um alerta importante:
      o arquivo de rotas ainda pode estar desatualizado (passando argumentos errados)
    """

    # Cria a conexão com o banco de dados
    db = get_db()
    
    # Cria o cursor para executar comandos SQL
    cursor = db.cursor()

    # Insere um novo administrador na tabela adm
    # O comando SQL usa placeholders (%s) para evitar SQL Injection
    cursor.execute("""
        INSERT INTO adm (nome, cpf, email, data_nascimento, login_id)
        VALUES (%s, %s, %s, %s, %s)
    """, (nome, cpf, email, data_nascimento, login_id))

    # Confirma a inserção no banco de dados
    db.commit()
    
    # Fecha a conexão com o banco (boa prática para liberar recursos)
    db.close()
    
    # Retorna True indicando que a operação foi bem-sucedida
    return True

    """
    Why password hashing needed:
    - Explicação conceitual sobre segurança de senhas

    - Security: Never store raw passwords.
      Nunca armazenar senha em texto puro (isso é uma falha grave de segurança)

    - Use salted hashes (Werkzeug PBKDF2 default).
      Usa hash com "sal" (proteção extra contra ataques), geralmente feito com Werkzeug

    - registrar_login(): generate_password_hash(senha) → secure storage.
      A função registrar_login gera o hash da senha antes de salvar no banco

    - login_user(): check_password_hash(hash, input) → validates without exposing.
      Na hora do login, a senha digitada é comparada com o hash armazenado

    Ensures correct DB save:
    - Explica o fluxo correto do sistema

    1. Routes call registrar_login(nome, senha, 1)
       → cria o login com senha criptografada
       → salva no banco
       → retorna o ID do login

    2. Insert profile with login_id → commit.
       → usa esse ID para inserir o perfil do ADM

    Both types (ADM=1, VENDEDOR=2) now consistent.
    - Agora tanto administrador quanto vendedor seguem o mesmo padrão de lógica
    """