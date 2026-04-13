# Importa a função responsável por conectar ao banco de dados
from database.connection import get_db

# Importa a função para gerar hash de senha (segurança)
from werkzeug.security import generate_password_hash

# Função para atualizar os dados de um vendedor
def atualizar_vendedor(id, nome, cpf, email, data_nascimento, login_nome=None, login_senha=None):
    """
    Atualiza os dados do vendedor.
    Se forem passados login_nome ou login_senha, atualiza também o login.
    """
    
    # Cria a conexão com o banco
    db = get_db()
    
    # Cria o cursor para executar comandos SQL
    cursor = db.cursor()

    # Atualiza dados do vendedor
    # Modifica os dados principais na tabela vendedor
    cursor.execute(
        """
        UPDATE vendedor
        SET nome=%s, cpf=%s, email=%s, data_nascimento=%s
        WHERE id=%s
        """,
        (nome, cpf, email, data_nascimento, id)
    )

    # Atualiza login, se fornecido
    # Só entra aqui se login_nome ou login_senha forem informados
    if login_nome or login_senha:
        
        # Busca o login_id associado ao vendedor
        cursor.execute("SELECT login_id FROM vendedor WHERE id=%s", (id,))
        
        # fetchone() retorna uma tupla → [0] pega o login_id
        login_id = cursor.fetchone()[0]

        # Se um novo nome de login foi fornecido
        if login_nome:
            
            # Atualiza o nome na tabela login
            cursor.execute(
                "UPDATE login SET nome=%s WHERE id=%s",
                (login_nome, login_id)
            )

        # Se uma nova senha foi fornecida
        if login_senha:
            
            # Gera o hash da senha (nunca salva senha em texto puro)
            senha_hash = generate_password_hash(login_senha)
            
            # Atualiza a senha com o hash
            cursor.execute(
                "UPDATE login SET senha=%s WHERE id=%s",
                (senha_hash, login_id)
            )

    # Confirma todas as alterações no banco
    db.commit()
    
    # Fecha a conexão com o banco
    db.close()