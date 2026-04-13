# Importa a função responsável por conectar ao banco de dados
from database.connection import get_db

# Função para inserir um item no estoque
def inserir_estoque(quantidade, preco, fornecedor_id):
    
    # conecta no banco
    db = get_db()
    
    # cria o cursor para executar comandos SQL
    cursor = db.cursor()

    # Converte a quantidade para inteiro
    # Isso garante que o valor esteja no tipo correto para operações matemáticas e banco
    quantidade = int(quantidade)
    
    # Converte o preço para float (número decimal)
    preco = float(preco)
    
    # Calcula o preço total de venda (quantidade * preço unitário)
    # OBS: essa variável está sendo calculada, mas NÃO está sendo usada depois
    preco_venda_total = quantidade * preco
    
    # insere item no estoque COM fornecedor
    # Executa um INSERT na tabela estoque
    # quantidade_calcas → quantidade de itens
    # preco_venda → preço unitário (ou de venda)
    # fornecedor_id → chave estrangeira que liga ao fornecedor
    cursor.execute(
        "INSERT INTO estoque (quantidade_calcas, preco_venda, fornecedor_id) VALUES (%s,%s,%s)",
        (quantidade, preco, fornecedor_id)
    )

    # Confirma a inserção no banco
    db.commit()
    
    # Fecha a conexão com o banco
    db.close()