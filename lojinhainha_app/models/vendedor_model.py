from database.connection import get_db


def listar_vendedores():

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM vendedor")
    dados = cursor.fetchall()

    db.close()
    return dados


def inserir_vendedor(nome, cpf, quantidade_vendas):

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "INSERT INTO vendedor (nome, cpf, quantidade_vendas) VALUES (%s,%s,%s)",
        (nome, cpf, quantidade_vendas)
    )

    db.commit()
    db.close()


def excluir_vendedor(id):

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("DELETE FROM vendedor WHERE id = %s", (id,))
    db.commit()

    db.close()