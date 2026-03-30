from database.connection import get_db

def inserir_vendedor(nome, cpf, email, data_nascimento):
    # conecta no banco
    db = get_db()
    cursor = db.cursor()

    # insere vendedor com novos campos
    cursor.execute(
        """
        INSERT INTO vendedor (nome, cpf, email, data_nascimento) 
        VALUES (%s,%s,%s,%s)
        """,
        (nome, cpf, email, data_nascimento)
    )

    db.commit()
    db.close()