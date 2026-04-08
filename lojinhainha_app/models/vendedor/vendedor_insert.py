from database.connection import get_db
from models.login_model import registrar_login

def inserir_vendedor(nome, cpf, email, data_nascimento, login_nome, login_senha):
    # conecta no banco
    db = get_db()
    cursor = db.cursor()

    # Primeiro, registra o login (tipo 2 = VENDEDOR)
    login_id = registrar_login(login_nome, login_senha, tipo_login=2)
    if not login_id:
        db.close()
        return False  # login já existe

    # insere vendedor com login_id
    cursor.execute(
        """
        INSERT INTO vendedor (nome, cpf, email, data_nascimento, login_id) 
        VALUES (%s,%s,%s,%s,%s)
        """,
        (nome, cpf, email, data_nascimento, login_id)
    )

    db.commit()
    db.close()
    return True