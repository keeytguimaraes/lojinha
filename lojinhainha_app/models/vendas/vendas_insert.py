from database.connection import get_db

def inserir_venda(cliente_id, vendedor_id, quantidade, cpf, preco, data, preco_total):
    db = get_db()
    cursor = db.cursor()

    quantidade = int(quantidade)
    preco = float(preco)
    preco_total = float(preco_total)

    cursor.execute(
        """INSERT INTO vendas 
        (vendedor_id, cliente_id, quantidade_vendas, cpf, preco, data, preco_total)
        VALUES (%s,%s,%s,%s,%s,%s,%s)""",
        (vendedor_id, cliente_id, quantidade, cpf, preco, data, preco_total)
    )

    db.commit()
    db.close()