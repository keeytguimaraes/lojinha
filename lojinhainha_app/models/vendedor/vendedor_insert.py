# Importa a função responsável por conectar ao banco de dados
from database.connection import get_db

# Função para inserir um novo vendedor
def inserir_vendedor(nome, cpf, email, data_nascimento, login_id):
    """
    Insere um novo vendedor na tabela 'vendedor'.
    Recebe login_id que referencia a tabela 'login'.
    """
    
    # Cria a conexão com o banco de dados
    db = get_db()
    
    # Cria o cursor para executar comandos SQL
    cursor = db.cursor()

    # Executa o comando INSERT para adicionar um novo vendedor
    # na tabela vendedor, incluindo a referência ao login (login_id)
    cursor.execute(
        """
        INSERT INTO vendedor (nome, cpf, email, data_nascimento, login_id)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (nome, cpf, email, data_nascimento, login_id)
    )

    # Confirma a inserção no banco de dados
    db.commit()
    
    # Fecha a conexão com o banco
    db.close()
    
    # Retorna True indicando que a operação foi bem-sucedida
    return True

    """
    Why password hashing needed:
    - Explicação conceitual sobre segurança de senhas

    - Security: Raw passwords in DB risky if breached.
      Senhas em texto puro são perigosas caso o banco seja comprometido

    - Hashing (PBKDF2 via Werkzeug) makes them irreversible.
      O uso de hash torna impossível recuperar a senha original

    - Handled in registrar_login(): generate_password_hash(senha)
      O hash é gerado antes de salvar no banco

    - Login validates with check_password_hash(stored_hash, input_senha).
      A validação compara a senha digitada com o hash armazenado

    Ensures DB persistence:
    - Explica o fluxo do sistema

    1. Routes: registrar_login() → hash → commit login record → get ID.
       Primeiro o login é criado com senha segura e retorna um ID

    2. This func: INSERT profile with login_id → commit.
       Depois o vendedor é inserido usando esse ID

    No transactions needed for simple flow.
    - Como são operações separadas e simples, não há necessidade de transação complexa
    """