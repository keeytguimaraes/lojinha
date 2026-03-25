from database.connection import get_db

def listar_estoque():
    # conecta no banco
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # busca estoque com nome do fornecedor
    cursor.execute("""
        SELECT 
            e.id, 
            e.quantidade_calcas, 
            e.preco_venda, 
            (e.quantidade_calcas * e.preco_venda) AS preco_venda_total,
            e.fornecedor_id,
            f.nome_empresa
        FROM estoque e
        JOIN fornecedor f ON e.fornecedor_id = f.id
    """)

    dados = cursor.fetchall()
    db.close()

    return dados