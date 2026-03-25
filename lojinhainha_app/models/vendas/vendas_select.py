from database.connection import get_db

def listar_vendas():
    """
    Busca todas as vendas no banco, trazendo também
    o nome do cliente e do vendedor relacionados.
    """
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT v.id, c.nome AS cliente, ve.nome AS vendedor,
               v.quantidade_vendas, v.preco, v.data
        FROM vendas v
        JOIN cliente c ON v.cliente_id = c.id
        JOIN vendedor ve ON v.vendedor_id = ve.id
    """)
    dados = cursor.fetchall()
    db.close()

    # ======= ADICIONAR CÁLCULO DO TOTAL =======
    for venda in dados:
        venda["preco_total"] = float(venda["quantidade_vendas"]) * float(venda["preco"])

    return dados