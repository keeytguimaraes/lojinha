from database.connection import get_db

def atualizar_vendedor(id, nome, cpf, email, data_nascimento):
    # conecta no banco
    db = get_db()
    cursor = db.cursor()

    # atualiza vendedor com novos campos
    cursor.execute(
        """
        UPDATE vendedor 
        SET nome=%s, cpf=%s, email=%s, data_nascimento=%s 
        WHERE id=%s
        """,
        (nome, cpf, email, data_nascimento, id)
    )

    db.commit()
    db.close()