from database.connection import get_db

def listar_vendedores():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT id, nome FROM vendedor")
    dados = cursor.fetchall()

    db.close()
    return dados


def inserir_estoque(quantidade, preco, vendedor_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "INSERT INTO estoque (quantidade_calcas, preco_venda, vendedor_id) VALUES (%s,%s,%s)",
        (quantidade, preco, vendedor_id)
    )

    db.commit()
    db.close()


def listar_estoque():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT e.id, e.quantidade_calcas, e.preco_venda, v.nome
        FROM estoque e
        JOIN vendedor v ON e.vendedor_id = v.id
    """)

    dados = cursor.fetchall()
    db.close()

    return dados


def excluir_estoque(id):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("DELETE FROM estoque WHERE id = %s", (id,))
    db.commit()

    db.close()