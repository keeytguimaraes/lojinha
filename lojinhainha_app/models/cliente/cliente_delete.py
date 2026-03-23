from database.connection import get_db

def excluir_cliente(id):
    # conecta no banco
    db = get_db()
    cursor = db.cursor()

    # remove cliente pelo id
    cursor.execute("DELETE FROM cliente WHERE id = %s", (id,))

    db.commit()
    db.close()