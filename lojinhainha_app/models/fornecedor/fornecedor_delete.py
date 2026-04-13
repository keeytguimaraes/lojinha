# Importa a função responsável por conectar ao banco de dados
from database.connection import get_db

# Função para excluir um fornecedor pelo ID
def excluir_fornecedor(id):
    
    # conecta no banco
    db = get_db()
    
    # cria o cursor com retorno em formato de dicionário
    # Isso permite acessar os resultados pelo nome da coluna
    cursor = db.cursor(dictionary=True)

    # pega endereço do fornecedor
    # Busca o endereco_id associado ao fornecedor
    cursor.execute("SELECT endereco_id FROM fornecedor WHERE id = %s", (id,))
    
    # fetchone() retorna um dicionário ou None
    resultado = cursor.fetchone()

    # Verifica se encontrou o fornecedor
    if resultado:
        
        # Acessa o endereco_id pelo nome da chave (por ser dictionary=True)
        endereco_id = resultado["endereco_id"]

        # remove fornecedor e endereço
        
        # Deleta o fornecedor da tabela fornecedor
        cursor.execute("DELETE FROM fornecedor WHERE id = %s", (id,))
        
        # Deleta o endereço associado ao fornecedor
        cursor.execute("DELETE FROM endereco WHERE id = %s", (endereco_id,))

        # Confirma as alterações no banco
        db.commit()

    # Fecha a conexão com o banco
    db.close()