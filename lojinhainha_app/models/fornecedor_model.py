from database.connection import get_db


def inserir_fornecedor(nome_empresa, cnpj, produto_quantidade, preco,
                       rua, bairro, numero, cidade):

    db = get_db()
    cursor = db.cursor(dictionary=True)

    # cria endereço
    cursor.execute(
        "INSERT INTO endereco (rua, bairro, numero, cidade) VALUES (%s,%s,%s,%s)",
        (rua, bairro, numero, cidade)
    )

    endereco_id = cursor.lastrowid

    # cria fornecedor
    cursor.execute(
        """INSERT INTO fornecedor 
        (nome_empresa, cnpj, produto_quantidade, preco, endereco_id) 
        VALUES (%s,%s,%s,%s,%s)""",
        (nome_empresa, cnpj, produto_quantidade, preco, endereco_id)
    )

    db.commit()
    db.close()


def listar_fornecedores():

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            f.id, f.nome_empresa, f.cnpj, f.produto_quantidade, f.preco,
            e.rua, e.bairro, e.numero, e.cidade
        FROM fornecedor f
        JOIN endereco e ON f.endereco_id = e.id
    """)

    dados = cursor.fetchall()
    db.close()

    return dados


def excluir_fornecedor(id):

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT endereco_id FROM fornecedor WHERE id = %s", (id,))
    resultado = cursor.fetchone()

    if resultado:
        endereco_id = resultado["endereco_id"]

        cursor.execute("DELETE FROM fornecedor WHERE id = %s", (id,))
        cursor.execute("DELETE FROM endereco WHERE id = %s", (endereco_id,))

        db.commit()

    db.close()