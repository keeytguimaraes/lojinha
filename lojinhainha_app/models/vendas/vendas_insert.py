from database.connection import get_db

def inserir_venda(cliente_id, vendedor_id, quantidade, cpf, preco, data):
    db = get_db()
    cursor = db.cursor()

    # converte os valores para garantir que são números
    quantidade = int(quantidade)
    preco = float(preco)
    preco_venda_total = quantidade * preco

    # insere venda (não salva total no banco)
    cursor.execute(
        """INSERT INTO vendas 
        (vendedor_id, cliente_id, quantidade_vendas, cpf, preco, data)
        VALUES (%s,%s,%s,%s,%s,%s)""",
        (vendedor_id, cliente_id, quantidade, cpf, preco, data)
    )

    db.commit()
    db.close()