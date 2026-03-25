from database.connection import get_db

def inserir_estoque(quantidade, preco, fornecedor_id):
    # conecta no banco
    db = get_db()
    cursor = db.cursor()

    quantidade = int(quantidade)
    preco = float(preco)
    preco_venda_total = quantidade * preco
    
    # insere item no estoque COM fornecedor
    cursor.execute(
        "INSERT INTO estoque (quantidade_calcas, preco_venda, fornecedor_id) VALUES (%s,%s,%s)",
        (quantidade, preco, fornecedor_id)
    )

    db.commit()
    db.close()