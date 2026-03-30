from database.connection import get_db

def excluir_cliente(id):
    db = get_db()
    cursor = db.cursor()

    # pega endereco_id antes de apagar
    cursor.execute("SELECT endereco_id FROM cliente WHERE id = %s", (id,))
    endereco = cursor.fetchone()

    # apaga vendas
    cursor.execute("DELETE FROM vendas WHERE cliente_id = %s", (id,))

    # apaga cliente
    cursor.execute("DELETE FROM cliente WHERE id = %s", (id,))

    # apaga endereço (se existir)
    if endereco:
        cursor.execute("DELETE FROM endereco WHERE id = %s", (endereco[0],))

    db.commit()
    db.close()