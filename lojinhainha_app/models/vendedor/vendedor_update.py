from database.connection import get_db

def atualizar_vendedor(id, nome, cpf):
    # conecta no banco
    db = get_db()
    cursor = db.cursor()

    # atualiza vendedor SEM quantidade_vendas
    cursor.execute(
        "UPDATE vendedor SET nome=%s, cpf=%s WHERE id=%s",
        (nome, cpf, id)
    )

    db.commit()
    db.close()