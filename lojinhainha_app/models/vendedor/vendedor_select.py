from database.connection import get_db

def listar_vendedores():
    """
    Lista todos os vendedores com dados de login.
    """
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
    SELECT vendedor.*, login.nome AS login_nome
    FROM vendedor
    JOIN login ON vendedor.login_id = login.id
    """)

    dados = cursor.fetchall()
    db.close()
    return dados