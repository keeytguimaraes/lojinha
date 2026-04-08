from database.connection import get_db
from models.login_model import registrar_login

def inserir_adm(nome, cpf, email, data_nascimento, login_nome, login_senha):
    db = get_db()
    cursor = db.cursor()

    # Primeiro cria login no sistema (tipo 1 = ADM)
    login_id = registrar_login(login_nome, login_senha, tipo_login=1)
    if not login_id:
        db.close()
        return False  # login já existe

    # Insere ADM com login_id
    cursor.execute("""
        INSERT INTO adm (nome, cpf, email, data_nascimento, login_id)
        VALUES (%s, %s, %s, %s, %s)
    """, (nome, cpf, email, data_nascimento, login_id))

    db.commit()
    db.close()
    return True