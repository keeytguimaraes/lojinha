from database.connection import get_db

def deletar_adm(id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("DELETE FROM adm WHERE id = %s", (id,))
    db.commit()