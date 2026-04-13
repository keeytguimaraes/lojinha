# Importa a função responsável por conectar ao banco de dados
from database.connection import get_db

# Função para deletar um vendedor, suas vendas e o login associado
def deletar_vendedor(id):
    """
    Deleta um vendedor, suas vendas e o login associado.
    """
    
    # Cria a conexão com o banco
    db = get_db()
    
    # Cria o cursor para executar comandos SQL
    cursor = db.cursor()

    try:
        # Busca o login_id do vendedor
        # Isso é necessário para deletar o login depois
        cursor.execute("SELECT login_id FROM vendedor WHERE id=%s", (id,))
        
        # fetchone() retorna uma tupla ou None
        resultado = cursor.fetchone()

        # Verifica se o vendedor existe
        if resultado:
            
            # Extrai o login_id da tupla
            login_id = resultado[0]

            # 1️⃣ Exclui vendas
            # Remove todas as vendas associadas ao vendedor
            # Isso evita erro de chave estrangeira ao deletar o vendedor
            cursor.execute("DELETE FROM vendas WHERE vendedor_id=%s", (id,))
            
            # 2️⃣ Exclui vendedor
            # Remove o vendedor da tabela vendedor
            cursor.execute("DELETE FROM vendedor WHERE id=%s", (id,))
            
            # 3️⃣ Exclui login
            # Remove o login associado ao vendedor
            cursor.execute("DELETE FROM login WHERE id=%s", (login_id,))
            
            # Confirma todas as alterações no banco
            db.commit()
        else:
            # Caso o vendedor não exista
            print("Vendedor não encontrado")

    except Exception as e:
        # Caso ocorra qualquer erro durante o processo
        
        # Desfaz todas as alterações feitas até o momento
        db.rollback()
        
        # Exibe mensagem de erro para debug
        print(f"Erro ao deletar vendedor: {e}")

    finally:
        # Fecha a conexão com o banco, independentemente de erro ou sucesso
        db.close()