from database.connection import get_db

def inserir_venda(cliente_id, vendedor_id, quantidade, cpf, preco, data):
    # conecta no banco
    db = get_db()
    cursor = db.cursor()

    # insere venda
    cursor.execute(
        """INSERT INTO vendas 
        (vendedor_id, cliente_id, quantidade_vendas, cpf, preco, data)
        VALUES (%s,%s,%s,%s,%s,%s)""",
        (vendedor_id, cliente_id, quantidade, cpf, preco, data)
    )

    db.commit()
    db.close()