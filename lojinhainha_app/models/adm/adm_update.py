from database.connection import get_db

def atualizar_adm(id, nome, cpf, email, data_nascimento):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        UPDATE adm
        SET nome = %s, cpf = %s, email = %s, data_nascimento = %s
        WHERE id = %s
    """, (nome, cpf, email, data_nascimento, id))

    db.commit()