# Importa a função responsável por conectar ao banco de dados
from database.connection import get_db

# Função para inserir uma nova venda
def inserir_venda(cliente_id, vendedor_id, quantidade, cpf, preco, data, preco_total):
    
    # Cria a conexão com o banco de dados
    db = get_db()
    
    # Cria o cursor para executar comandos SQL
    cursor = db.cursor()

    # Converte a quantidade para inteiro
    # Garante que o valor esteja no tipo correto
    quantidade = int(quantidade)
    
    # Converte o preço para float (valor decimal)
    preco = float(preco)
    
    # Converte o preço total para float
    preco_total = float(preco_total)

    # Executa o comando INSERT para adicionar uma nova venda
    # na tabela vendas com todos os dados necessários
    cursor.execute(
        """INSERT INTO vendas 
        (vendedor_id, cliente_id, quantidade_vendas, cpf, preco, data, preco_total)
        VALUES (%s,%s,%s,%s,%s,%s,%s)""",
        (vendedor_id, cliente_id, quantidade, cpf, preco, data, preco_total)
    )

    # Confirma a inserção no banco de dados
    db.commit()
    
    # Fecha a conexão com o banco
    db.close()