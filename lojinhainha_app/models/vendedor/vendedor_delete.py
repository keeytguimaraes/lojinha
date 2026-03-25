from database.connection import get_db

def excluir_vendedor(id):
    db = get_db()
    cursor = db.cursor()

    # remove primeiro as vendas desse vendedor
    cursor.execute("DELETE FROM vendas WHERE vendedor_id = %s", (id,))

    # depois remove o vendedor
    cursor.execute("DELETE FROM vendedor WHERE id = %s", (id,))

    db.commit()
    db.close()