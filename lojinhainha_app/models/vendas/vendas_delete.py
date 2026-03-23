from database.connection import get_db

def excluir_venda(id):
    # conecta no banco
    db = get_db()
    cursor = db.cursor()

    # remove venda
    cursor.execute("DELETE FROM vendas WHERE id = %s", (id,))

    db.commit()
    db.close()