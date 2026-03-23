from database.connection import get_db

def atualizar_venda(id, quantidade, preco):
    # conecta no banco
    db = get_db()
    cursor = db.cursor()

    # atualiza venda
    cursor.execute(
        "UPDATE vendas SET quantidade_vendas=%s, preco=%s WHERE id=%s",
        (quantidade, preco, id)
    )

    db.commit()
    db.close()