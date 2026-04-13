# Importa a função que cria conexão com o banco de dados
from database.connection import get_db

# Função para excluir um cliente com base no ID
def excluir_cliente(id):
    
    # Cria conexão com o banco
    db = get_db()
    
    # Cria o cursor para executar comandos SQL
    cursor = db.cursor()

    # pega endereco_id antes de apagar
    # Aqui buscamos o endereço associado ao cliente
    # Isso é necessário porque depois que o cliente for deletado,
    # não teremos mais acesso a esse dado
    cursor.execute("SELECT endereco_id FROM cliente WHERE id = %s", (id,))
    
    # fetchone() retorna uma tupla ou None
    endereco = cursor.fetchone()

    # apaga vendas
    # Remove todos os registros da tabela vendas que pertencem a esse cliente
    # Isso evita erro de chave estrangeira (FK) ao deletar o cliente depois
    cursor.execute("DELETE FROM vendas WHERE cliente_id = %s", (id,))

    # apaga cliente
    # Remove o cliente da tabela cliente
    cursor.execute("DELETE FROM cliente WHERE id = %s", (id,))

    # apaga endereço (se existir)
    # Verifica se o cliente tinha um endereço associado
    if endereco:
        
        # endereco[0] pega o id do endereço dentro da tupla retornada
        cursor.execute("DELETE FROM endereco WHERE id = %s", (endereco[0],))

    # Confirma todas as alterações feitas no banco
    db.commit()
    
    # Fecha a conexão com o banco
    db.close()