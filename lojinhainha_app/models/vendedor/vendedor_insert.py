from database.connection import get_db

def inserir_vendedor(nome, cpf):
    # conecta no banco
    db = get_db()
    cursor = db.cursor()

    # insere vendedor SEM quantidade_vendas
    cursor.execute(
        "INSERT INTO vendedor (nome, cpf) VALUES (%s,%s)",
        (nome, cpf)
    )

    db.commit()
    db.close()