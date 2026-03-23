from database.connection import get_db

def listar_clientes():
    # conecta no banco
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # busca clientes com endereço
    cursor.execute("""
        SELECT 
            c.id, c.nome, c.cpf,
            e.rua, e.bairro, e.numero, e.cidade
        FROM cliente c
        JOIN endereco e ON c.endereco_id = e.id
    """)

    dados = cursor.fetchall()
    db.close()

    return dados