from database.connection import get_db

def listar_estoque():
    # conecta no banco
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # busca estoque com nome do vendedor
    cursor.execute("""
       SELECT 
    e.id, 
    e.quantidade_calcas, 
    e.preco_venda, 
    (e.quantidade_calcas * e.preco_venda) AS preco_venda_total,
    e.vendedor_id,
    v.nome
FROM estoque e
JOIN vendedor v ON e.vendedor_id = v.id
    """)

    dados = cursor.fetchall()
    db.close()

    return dados