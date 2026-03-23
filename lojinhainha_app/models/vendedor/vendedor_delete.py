from database.connection import get_db

def excluir_vendedor(id):
    # conecta no banco
    db = get_db()
    cursor = db.cursor()

    # remove vendedor
    cursor.execute("DELETE FROM vendedor WHERE id = %s", (id,))

    db.commit()
    db.close()