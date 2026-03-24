from database.connection import get_db

def inserir_fornecedor(nome_empresa, cnpj, produto_quantidade, preco, rua, bairro, numero, cidade, complemento):
    # conecta no banco
    db = get_db()
    cursor = db.cursor()

    # cria endereço
    cursor.execute(
        cursor.execute(
    "INSERT INTO endereco (rua, bairro, numero, cidade, complemento) VALUES (%s,%s,%s,%s,%s)",
    (rua, bairro, numero, cidade, complemento)
)
    )

    endereco_id = cursor.lastrowid

    produto_quantidade = int(produto_quantidade)
    preco = float(preco)

    preco_total = produto_quantidade * preco
    # cria fornecedor
    cursor.execute(
        """INSERT INTO fornecedor 
        (nome_empresa, cnpj, produto_quantidade, preco, endereco_id, preco_total) 
        VALUES (%s,%s,%s,%s,%s,%s)""",
        (nome_empresa, cnpj, produto_quantidade, preco, endereco_id, preco_total)
    )

    db.commit()
    db.close()