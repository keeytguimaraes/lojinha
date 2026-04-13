# Importa a função responsável por conectar ao banco de dados
from database.connection import get_db

# Função para atualizar um item do estoque
def atualizar_estoque(id, quantidade, preco, fornecedor_id):
    
    # conecta no banco
    db = get_db()
    
    # cria o cursor para executar comandos SQL
    cursor = db.cursor()

    # Converte a quantidade para inteiro
    # Garante que o valor esteja no tipo correto
    quantidade = int(quantidade)
    
    # Converte o preço para float
    preco = float(preco)
    
    # Calcula o valor total (quantidade * preço)
    # OBS: novamente essa variável é calculada, mas NÃO está sendo usada depois
    preco_venda_total = quantidade * preco 
    
    # atualiza item do estoque COM fornecedor
    # Atualiza os dados na tabela estoque com base no ID
    cursor.execute(
        "UPDATE estoque SET quantidade_calcas=%s, preco_venda=%s, fornecedor_id=%s WHERE id=%s",
        (quantidade, preco, fornecedor_id, id)
    )

    # Confirma as alterações no banco
    db.commit()
    
    # Fecha a conexão com o banco
    db.close()