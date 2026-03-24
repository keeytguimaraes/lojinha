from database.connection import get_db

def excluir_cliente(id):
    # conecta no banco
    db = get_db()
    cursor = db.cursor()

    # APAGA PRIMEIRO AS VENDAS
    cursor.execute("DELETE FROM vendas WHERE cliente_id = %s", (id,))

    #  DEPOIS APAGA O CLIENTE
    cursor.execute("DELETE FROM cliente WHERE id = %s", (id,))

    db.commit()
    db.close()