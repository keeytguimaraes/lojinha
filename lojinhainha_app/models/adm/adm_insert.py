from database.connection import get_db

def inserir_adm(nome, cpf, email, data_nascimento):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO adm (nome, cpf, email, data_nascimento)
        VALUES (%s, %s, %s, %s)
    """, (nome, cpf, email, data_nascimento))

    db.commit()