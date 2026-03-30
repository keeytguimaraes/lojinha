from database.connection import get_db

def inserir_cliente(nome, cpf, email, data_nascimento, rua, bairro, numero, cidade, complemento):
    # cria conexão com banco
    db = get_db()
    cursor = db.cursor()

    # insere endereço do cliente
    cursor.execute(
        """
        INSERT INTO endereco (rua, bairro, numero, cidade, complemento) 
        VALUES (%s,%s,%s,%s,%s)
        """,
        (rua, bairro, numero, cidade, complemento)
    )

    # pega id do endereço criado
    endereco_id = cursor.lastrowid

    # insere cliente com o endereço + novos campos
    cursor.execute(
        """
        INSERT INTO cliente (nome, cpf, email, data_nascimento, endereco_id) 
        VALUES (%s,%s,%s,%s,%s)
        """,
        (nome, cpf, email, data_nascimento, endereco_id)
    )

    # salva alterações
    db.commit()
    db.close()