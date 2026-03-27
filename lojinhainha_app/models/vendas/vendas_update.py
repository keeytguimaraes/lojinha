from database.connection import get_db

def atualizar_venda(id, cliente_id, vendedor_id, quantidade, fornecedor_id):
    db = get_db()
    cursor = db.cursor()

    quantidade = int(quantidade)

    # BUSCAR PREÇO DO FORNECEDOR
    cursor.execute("SELECT preco FROM fornecedor WHERE id = %s", (fornecedor_id,))
    fornecedor = cursor.fetchone()

    preco_fornecedor = float(fornecedor[0]) if fornecedor else 0

    #  CALCULAR
    preco_unitario = preco_fornecedor * 1.2
    preco_total = preco_unitario * quantidade

    #  ATUALIZA TUDO
    cursor.execute(
        """UPDATE vendas 
           SET cliente_id=%s, vendedor_id=%s, quantidade_vendas=%s, preco=%s, preco_total=%s 
           WHERE id=%s""",
        (cliente_id, vendedor_id, quantidade, preco_unitario, preco_total, id)
    )

    db.commit()
    db.close()