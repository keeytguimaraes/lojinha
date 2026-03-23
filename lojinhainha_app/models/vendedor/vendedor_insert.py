from database.connection import get_db

def inserir_vendedor(nome, cpf, quantidade):
    # conecta no banco
    db = get_db()
    cursor = db.cursor()

    # insere vendedor
    cursor.execute(
        "INSERT INTO vendedor (nome, cpf, quantidade_vendas) VALUES (%s,%s,%s)",
        (nome, cpf, quantidade)
    )

    db.commit()
    db.close()