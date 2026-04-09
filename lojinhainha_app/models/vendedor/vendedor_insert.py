from database.connection import get_db

def inserir_vendedor(nome, cpf, email, data_nascimento, login_id):
    """
    Insere um novo vendedor na tabela 'vendedor'.
    Recebe login_id que referencia a tabela 'login'.
    """
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO vendedor (nome, cpf, email, data_nascimento, login_id)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (nome, cpf, email, data_nascimento, login_id)
    )

    db.commit()
    db.close()
    return True
    """
    Why password hashing needed:
    - Security: Raw passwords in DB risky if breached. Hashing (PBKDF2 via Werkzeug) makes them irreversible.
    - Handled in registrar_login(): generate_password_hash(senha) before INSERT + commit.
    - Login validates with check_password_hash(stored_hash, input_senha).
    
    Ensures DB persistence:
    1. Routes: registrar_login() → hash → commit login record → get ID.
    2. This func: INSERT profile with login_id → commit.
    No transactions needed for simple flow.
    """
