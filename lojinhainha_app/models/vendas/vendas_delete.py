from database.connection import get_db

def excluir_venda(id):
    db = get_db()
    cursor = db.cursor()

    #  verifica se a venda existe antes de excluir
    cursor.execute("SELECT id FROM vendas WHERE id = %s", (id,))
    venda = cursor.fetchone()

    if venda:
        cursor.execute("DELETE FROM vendas WHERE id = %s", (id,))
        db.commit()

    db.close()