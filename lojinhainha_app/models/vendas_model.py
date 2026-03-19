from database.connection import get_db


def listar_clientes():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT id, nome FROM cliente")
    dados = cursor.fetchall()

    db.close()
    return dados


def listar_vendedores():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT id, nome FROM vendedor")
    dados = cursor.fetchall()

    db.close()
    return dados


def inserir_venda(cliente_id, vendedor_id, quantidade, cpf, preco, data):

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        """
        INSERT INTO vendas (vendedor_id, cliente_id, quantidade_vendas, cpf, preco, data)
        VALUES (%s,%s,%s,%s,%s,%s)
        """,
        (vendedor_id, cliente_id, quantidade, cpf, preco, data)
    )

    db.commit()
    db.close()


def listar_vendas():

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT v.id, c.nome AS cliente, ve.nome AS vendedor,
               v.quantidade_vendas, v.preco, v.data
        FROM vendas v
        JOIN cliente c ON v.cliente_id = c.id
        JOIN vendedor ve ON v.vendedor_id = ve.id
    """)

    dados = cursor.fetchall()
    db.close()

    return dados


def excluir_venda(id):

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("DELETE FROM vendas WHERE id = %s", (id,))
    db.commit()

    db.close()