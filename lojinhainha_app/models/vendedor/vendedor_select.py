from database.connection import get_db

def listar_vendedores():
    # conecta no banco
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # busca todos vendedores
    cursor.execute("SELECT * FROM vendedor")

    dados = cursor.fetchall()
    db.close()

    return dados