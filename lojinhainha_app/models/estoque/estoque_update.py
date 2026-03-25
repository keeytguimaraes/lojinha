from database.connection import get_db

def atualizar_estoque(id, quantidade, preco, fornecedor_id):
    # conecta no banco
    db = get_db()
    cursor = db.cursor()

    quantidade = int(quantidade)
    preco = float(preco)
    preco_venda_total = quantidade * preco 
    
    # atualiza item do estoque COM fornecedor
    cursor.execute(
        "UPDATE estoque SET quantidade_calcas=%s, preco_venda=%s, fornecedor_id=%s WHERE id=%s",
        (quantidade, preco, fornecedor_id, id)
    )

    db.commit()
    db.close()