from database.connection import get_db


def inserir_cliente(nome, cpf, rua, bairro, numero, cidade):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO endereco (rua, bairro, numero, cidade) VALUES (%s,%s,%s,%s)",
        (rua, bairro, numero, cidade)
    )

    endereco_id = cursor.lastrowid

    cursor.execute(
        "INSERT INTO cliente (nome, cpf, endereco_id) VALUES (%s,%s,%s)",
        (nome, cpf, endereco_id)
    )

    db.commit()
    db.close()


def listar_clientes():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            c.id,
            c.nome,
            c.cpf,
            e.rua,
            e.bairro,
            e.numero,
            e.cidade
        FROM cliente c
        JOIN endereco e ON c.endereco_id = e.id
    """)

    dados = cursor.fetchall()
    db.close()

    return dados


def excluir_cliente(id):
    db = get_db()
    cursor = db.cursor()

    # deletar cliente direto
    cursor.execute("DELETE FROM cliente WHERE id = %s", (id,))
    db.commit()

    db.close()