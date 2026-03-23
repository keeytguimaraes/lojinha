from database.connection import get_db

def atualizar_estoque(id, quantidade, preco, vendedor_id):
    # conecta no banco
    db = get_db()
    cursor = db.cursor()

    # atualiza item do estoque
    cursor.execute(
        "UPDATE estoque SET quantidade_calcas=%s, preco_venda=%s, vendedor_id=%s WHERE id=%s",
        (quantidade, preco, vendedor_id, id)
    )

    db.commit()
    db.close()