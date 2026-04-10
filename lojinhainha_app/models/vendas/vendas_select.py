from database.connection import get_db

def listar_vendas():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
    v.id,
    c.nome AS cliente,
    ve.nome AS vendedor,
    v.quantidade_vendas,
    v.preco,
    v.preco_total,
    v.data
    FROM vendas v
    JOIN cliente c ON v.cliente_id = c.id
    JOIN login ve ON v.vendedor_id = ve.id;
    """)

    dados = cursor.fetchall()
    db.close()

    return dados