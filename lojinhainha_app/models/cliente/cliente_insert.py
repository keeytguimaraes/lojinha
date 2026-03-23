from database.connection import get_db

def inserir_cliente(nome, cpf, rua, bairro, numero, cidade):
    # cria conexão com banco
    db = get_db()
    cursor = db.cursor()

    # insere endereço do cliente
    cursor.execute(
        "INSERT INTO endereco (rua, bairro, numero, cidade) VALUES (%s,%s,%s,%s)",
        (rua, bairro, numero, cidade)
    )

    # pega id do endereço criado
    endereco_id = cursor.lastrowid

    # insere cliente com o endereço
    cursor.execute(
        "INSERT INTO cliente (nome, cpf, endereco_id) VALUES (%s,%s,%s)",
        (nome, cpf, endereco_id)
    )

    # salva alterações
    db.commit()
    db.close()