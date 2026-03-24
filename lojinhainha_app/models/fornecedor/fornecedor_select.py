from database.connection import get_db

def listar_fornecedores():
    # conecta no banco
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # busca fornecedores com endereço
    cursor.execute("""
        SELECT f.id, f.nome_empresa, f.cnpj, 
               f.produto_quantidade, f.preco, f.preco_total,
               e.rua, e.bairro, e.numero, e.cidade
        FROM fornecedor f
        JOIN endereco e ON f.endereco_id = e.id
    """)

    dados = cursor.fetchall()
    db.close()

    return dados