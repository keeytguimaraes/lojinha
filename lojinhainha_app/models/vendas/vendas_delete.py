# Importa a função responsável por conectar ao banco de dados
from database.connection import get_db

# Função para excluir uma venda pelo ID
def excluir_venda(id):
    
    # Cria a conexão com o banco
    db = get_db()
    
    # Cria o cursor para executar comandos SQL
    cursor = db.cursor()

    # verifica se a venda existe antes de excluir
    # Executa uma consulta para buscar o ID da venda
    # Isso evita tentar deletar algo que não existe
    cursor.execute("SELECT id FROM vendas WHERE id = %s", (id,))
    
    # fetchone() retorna uma tupla ou None
    venda = cursor.fetchone()

    # Se a venda existir no banco
    if venda:
        
        # Executa o comando DELETE para remover a venda
        cursor.execute("DELETE FROM vendas WHERE id = %s", (id,))
        
        # Confirma a exclusão no banco
        db.commit()

    # Fecha a conexão com o banco
    db.close()