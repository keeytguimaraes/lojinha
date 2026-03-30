from database.connection import get_db

def atualizar_cliente(id, nome, cpf, email, data_nascimento, rua, bairro, numero, cidade, complemento):
    # conecta no banco
    db = get_db()
    cursor = db.cursor()

    # atualiza dados do cliente
    cursor.execute(
        """
        UPDATE cliente 
        SET nome=%s, cpf=%s, email=%s, data_nascimento=%s 
        WHERE id=%s
        """,
        (nome, cpf, email, data_nascimento, id)
    )

    # pega id do endereço relacionado
    cursor.execute("SELECT endereco_id FROM cliente WHERE id = %s", (id,))
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