# Importa a função get_db do módulo database.connection
# Essa função é responsável por criar e retornar uma conexão com o banco de dados
from database.connection import get_db

# Define uma função chamada deletar_adm que recebe como parâmetro o id do administrador
def deletar_adm(id):
    
    # Cria a conexão com o banco de dados chamando a função get_db()
    db = get_db()
    
    # Cria um cursor, que é o objeto usado para executar comandos SQL no banco
    cursor = db.cursor()

    # 1️⃣ Pegar o login_id do ADM antes de deletar
    # Executa uma consulta SQL para buscar o login_id na tabela adm
    # O %s é um placeholder para evitar SQL Injection (boa prática de segurança)
    # (id,) é uma tupla com o valor que será substituído no lugar do %s
    cursor.execute("SELECT login_id FROM adm WHERE id = %s", (id,))
    
    # Pega o resultado da consulta (uma única linha)
    resultado = cursor.fetchone()

    # Verifica se encontrou algum resultado no banco
    if resultado:
        
        # Acessa o primeiro valor da tupla retornada (login_id)
        login_id = resultado[0]

        # 2️⃣ Deletar o ADM
        # Executa o comando SQL para deletar o administrador da tabela adm
        cursor.execute("DELETE FROM adm WHERE id = %s", (id,))
        
        # Confirma a alteração no banco de dados (sem isso, o delete não é salvo)
        db.commit()

        # 3️⃣ Deletar também o login associado
        # Executa o comando SQL para deletar o login relacionado ao administrador
        # usando o login_id que foi buscado anteriormente
        cursor.execute("DELETE FROM login WHERE id = %s", (login_id,))
        
        # Confirma novamente a alteração no banco
        db.commit()