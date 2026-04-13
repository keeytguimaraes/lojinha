# Importa a função de conexão com o banco de dados
from database.connection import get_db

# Importa a função responsável por gerar hash de senha (segurança)
from werkzeug.security import generate_password_hash

# Função para atualizar um administrador
# Recebe os dados do ADM e opcionalmente dados de login
def atualizar_adm(id, nome, cpf, email, data_nascimento, login_nome=None, login_senha=None):
    
    # Cria conexão com o banco
    db = get_db()
    
    # Cria o cursor para executar comandos SQL
    cursor = db.cursor()

    # Atualiza os dados principais do administrador na tabela adm
    cursor.execute("""
        UPDATE adm
        SET nome=%s, cpf=%s, email=%s, data_nascimento=%s
        WHERE id=%s
    """, (nome, cpf, email, data_nascimento, id))

    # Verifica se foi enviado login_nome ou login_senha
    # Isso evita atualizar o login sem necessidade
    if login_nome or login_senha:
        
        # Busca o login_id relacionado a esse administrador
        cursor.execute("SELECT login_id FROM adm WHERE id=%s", (id,))
        
        # fetchone() retorna uma tupla → [0] pega o primeiro valor (login_id)
        login_id = cursor.fetchone()[0]

        # Se um novo nome de login foi fornecido
        if login_nome:
            
            # Atualiza o nome de login na tabela login
            cursor.execute(
                "UPDATE login SET nome=%s WHERE id=%s",
                (login_nome, login_id)
            )

        # Se uma nova senha foi fornecida
        if login_senha:
            
            # Gera o hash da senha (NUNCA salva senha pura)
            senha_hash = generate_password_hash(login_senha)
            
            # Atualiza a senha no banco com o hash
            cursor.execute(
                "UPDATE login SET senha=%s WHERE id=%s",
                (senha_hash, login_id)
            )

    # Confirma todas as alterações no banco
    db.commit()
    
    # Fecha a conexão
    db.close()