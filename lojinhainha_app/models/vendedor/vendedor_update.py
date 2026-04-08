from database.connection import get_db
from werkzeug.security import generate_password_hash

def atualizar_vendedor(id, nome, cpf, email, data_nascimento, login_nome=None, login_senha=None):
    db = get_db()
    cursor = db.cursor()

    # Atualiza dados do vendedor
    cursor.execute(
        """
        UPDATE vendedor 
        SET nome=%s, cpf=%s, email=%s, data_nascimento=%s 
        WHERE id=%s
        """,
        (nome, cpf, email, data_nascimento, id)
    )

    # Atualiza login se fornecido
    if login_nome or login_senha:
        # pega o login_id do vendedor
        cursor.execute("SELECT login_id FROM vendedor WHERE id=%s", (id,))
        login_id = cursor.fetchone()[0]

        if login_nome:
            cursor.execute("UPDATE login SET nome=%s WHERE id=%s", (login_nome, login_id))
        if login_senha:
            senha_hash = generate_password_hash(login_senha)
            cursor.execute("UPDATE login SET senha=%s WHERE id=%s", (senha_hash, login_id))

    db.commit()
    db.close()