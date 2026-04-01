from database.connection import get_db

def listar_adms():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM adm")
    return cursor.fetchall()


def buscar_adm_por_id(id):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM adm WHERE id = %s", (id,))
    return cursor.fetchone()