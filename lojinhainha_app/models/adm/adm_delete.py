from database.connection import get_db

def deletar_adm(id):
    db = get_db()
    cursor = db.cursor()

    # 1️⃣ Pegar o login_id do ADM antes de deletar
    cursor.execute("SELECT login_id FROM adm WHERE id = %s", (id,))
    resultado = cursor.fetchone()

    if resultado:
        login_id = resultado[0]

        # 2️⃣ Deletar o ADM
        cursor.execute("DELETE FROM adm WHERE id = %s", (id,))
        db.commit()

        # 3️⃣ Deletar também o login associado
        cursor.execute("DELETE FROM login WHERE id = %s", (login_id,))
        db.commit()