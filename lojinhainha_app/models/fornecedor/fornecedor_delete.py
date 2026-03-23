from database.connection import get_db

def excluir_fornecedor(id):
    # conecta no banco
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # pega endereço do fornecedor
    cursor.execute("SELECT endereco_id FROM fornecedor WHERE id = %s", (id,))
    resultado = cursor.fetchone()

    if resultado:
        endereco_id = resultado["endereco_id"]

        # remove fornecedor e endereço
        cursor.execute("DELETE FROM fornecedor WHERE id = %s", (id,))
        cursor.execute("DELETE FROM endereco WHERE id = %s", (endereco_id,))

        db.commit()

    db.close()