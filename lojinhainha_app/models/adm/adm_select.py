from database.connection import get_db

def listar_adms():
    """
    Lista todos os administradores com dados de login.
    """
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            a.id, a.nome, a.cpf, a.email, a.data_nascimento,
            l.nome AS login_nome
        FROM adm a
        JOIN login l ON a.login_id = l.id
    """)

    dados = cursor.fetchall()
    db.close()
    return dados


def buscar_adm_por_id(id):
    """
    Busca um administrador pelo ID.
    """
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM adm WHERE id = %s",
        (id,)
    )

    dado = cursor.fetchone()
    db.close()
    return dado