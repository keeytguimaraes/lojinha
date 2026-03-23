from database.connection import get_db

def atualizar_vendedor(id, nome, cpf, quantidade):
    # conecta no banco
    db = get_db()
    cursor = db.cursor()

    # atualiza vendedor
    cursor.execute(
        "UPDATE vendedor SET nome=%s, cpf=%s, quantidade_vendas=%s WHERE id=%s",
        (nome, cpf, quantidade, id)
    )

    db.commit()
    db.close()