from database.connection import get_db

def atualizar_venda(id, cliente_id, vendedor_id, quantidade, preco):
    db = get_db()
    cursor = db.cursor()

    quantidade = int(quantidade)
    preco = float(preco)

    # atualiza venda
    cursor.execute(
        """UPDATE vendas 
           SET cliente_id=%s, vendedor_id=%s, quantidade_vendas=%s, preco=%s 
           WHERE id=%s""",
        (cliente_id, vendedor_id, quantidade, preco, id)
    )

    db.commit()
    db.close()