# Importa a função responsável por criar conexão com o banco de dados
from database.connection import get_db

# Função para excluir um item do estoque pelo ID
def excluir_estoque(id):
    
    # conecta no banco
    db = get_db()
    
    # cria o cursor para executar comandos SQL
    cursor = db.cursor()

    # remove item do estoque pelo ID
    # Executa um comando DELETE na tabela estoque
    # WHERE id = %s garante que apenas o item específico será removido
    # (id,) é uma tupla → protege contra SQL Injection
    cursor.execute("DELETE FROM estoque WHERE id = %s", (id,))

    # Confirma a exclusão no banco de dados
    db.commit()
    
    # Fecha a conexão com o banco
    db.close()