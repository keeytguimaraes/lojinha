from database.connection import get_db

def atualizar_fornecedor(id, nome, cnpj, quantidade, preco):
    # conecta no banco
    db = get_db()
    cursor = db.cursor()

    quantidade = int(quantidade)
    preco = float(preco.replace(",", "."))  
    preco_total = quantidade * preco

    # atualiza fornecedor
    cursor.execute(
        """UPDATE fornecedor 
        SET nome_empresa=%s, cnpj=%s, produto_quantidade=%s, preco=%s, preco_total=%s 
        WHERE id=%s""",
        (nome, cnpj, quantidade, preco, preco_total, id)
    )

    db.commit()
    db.close()