from database.connection import get_db

def listar_vendedores():
    """
    Lista todos os vendedores com dados de login.
    """
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
    v.id,
    v.nome,
    v.cpf,
    v.email,
    v.data_nascimento
    FROM vendedor v
    """)

    dados = cursor.fetchall()
    db.close()
    return dados