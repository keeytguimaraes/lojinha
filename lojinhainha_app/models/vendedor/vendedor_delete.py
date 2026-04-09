from database.connection import get_db

def deletar_vendedor(id):
    """
    Deleta um vendedor, suas vendas e o login associado.
    """
    db = get_db()
    cursor = db.cursor()

    try:
        # Busca o login_id do vendedor
        cursor.execute("SELECT login_id FROM vendedor WHERE id=%s", (id,))
        resultado = cursor.fetchone()

        if resultado:
            login_id = resultado[0]

            # 1️⃣ Exclui vendas
            cursor.execute("DELETE FROM vendas WHERE vendedor_id=%s", (id,))
            # 2️⃣ Exclui vendedor
            cursor.execute("DELETE FROM vendedor WHERE id=%s", (id,))
            # 3️⃣ Exclui login
            cursor.execute("DELETE FROM login WHERE id=%s", (login_id,))
            db.commit()
        else:
            print("Vendedor não encontrado")
    except Exception as e:
        db.rollback()
        print(f"Erro ao deletar vendedor: {e}")
    finally:
        db.close()