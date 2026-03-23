from database.connection import get_db

def atualizar_cliente(id, nome, cpf, rua, bairro, numero, cidade):
    # conecta no banco
    db = get_db()
    cursor = db.cursor()

    # atualiza dados do cliente
    cursor.execute(
        "UPDATE cliente SET nome=%s, cpf=%s WHERE id=%s",
        (nome, cpf, id)
    )

    # pega id do endereço relacionado
    cursor.execute("SELECT endereco_id FROM cliente WHERE id = %s", (id,))
    endereco_id = cursor.fetchone()[0]

    # atualiza endereço
    cursor.execute(
        "UPDATE endereco SET rua=%s, bairro=%s, numero=%s, cidade=%s WHERE id=%s",
        (rua, bairro, numero, cidade, endereco_id)
    )

    db.commit()
    db.close()