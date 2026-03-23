from database.connection import get_db

def atualizar_fornecedor(id, nome, cnpj, quantidade, preco):
    # conecta no banco
    db = get_db()
    cursor = db.cursor()

    # atualiza fornecedor
    cursor.execute(
        """UPDATE fornecedor 
        SET nome_empresa=%s, cnpj=%s, produto_quantidade=%s, preco=%s 
        WHERE id=%s""",
        (nome, cnpj, quantidade, preco, id)
    )

    db.commit()
    db.close()