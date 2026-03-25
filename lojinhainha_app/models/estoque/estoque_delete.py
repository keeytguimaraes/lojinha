from database.connection import get_db

def excluir_estoque(id):
    # conecta no banco
    db = get_db()
    cursor = db.cursor()

    # remove item do estoque pelo ID
    cursor.execute("DELETE FROM estoque WHERE id = %s", (id,))

    db.commit()
    db.close()