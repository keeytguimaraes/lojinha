from database.connection import get_db

def atualizar_fornecedor(id, nome, cnpj, quantidade, preco, rua, bairro, numero, cidade, complemento):
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
     # pega id do endereço relacionado
    cursor.execute("SELECT endereco_id FROM fornecedor WHERE id = %s", (id,))
    endereco_id = cursor.fetchone()[0]

    # atualiza endereço
    cursor.execute(
        """
        UPDATE endereco 
        SET rua=%s, bairro=%s, numero=%s, cidade=%s, complemento=%s 
        WHERE id=%s
        """,
        (rua, bairro, numero, cidade, complemento, endereco_id)
    )

    db.commit()
    db.close()