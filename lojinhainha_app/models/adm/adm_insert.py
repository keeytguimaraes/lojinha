from database.connection import get_db
# from models.login_model import registrar_login  # Removed

def inserir_adm(nome, cpf, email, data_nascimento, login_id):
    """
     FIX: Updated to use pre-registered login_id.
    - Matches pattern of vendedor_insert.
    - Routes should call registrar_login first, then this.
    Note: adm_routes.py currently passes 4 args — needs route fix if used.
    """
    db = get_db()
    cursor = db.cursor()

    # Insere ADM com login_id
    cursor.execute("""
        INSERT INTO adm (nome, cpf, email, data_nascimento, login_id)
        VALUES (%s, %s, %s, %s, %s)
    """, (nome, cpf, email, data_nascimento, login_id))

    db.commit()
    db.close()
    return True

    """
    Why password hashing needed:
    - Security: Never store raw passwords. Use salted hashes (Werkzeug PBKDF2 default).
    - registrar_login(): generate_password_hash(senha) → secure storage.
    - login_user(): check_password_hash(hash, input) → validates without exposing.

    Ensures correct DB save:
    1. Routes call registrar_login(nome, senha, 1) → hash → commit login → return ID.
    2. Insert profile with login_id → commit.
    Both types (ADM=1, VENDEDOR=2) now consistent.
    """
