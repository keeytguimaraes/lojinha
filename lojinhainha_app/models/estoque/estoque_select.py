# Importa a função responsável por conectar ao banco de dados
from database.connection import get_db

# Função para listar os itens do estoque
def listar_estoque():
    
    # conecta no banco
    db = get_db()
    
    # cria o cursor com retorno em formato de dicionário
    # Isso facilita o uso dos dados no frontend (HTML, templates, etc.)
    cursor = db.cursor(dictionary=True)

    # busca estoque com nome do fornecedor
    # Aqui usamos JOIN para relacionar estoque com fornecedor
    cursor.execute("""
        SELECT 
            e.id, 
            e.quantidade_calcas, 
            e.preco_venda, 
            
            # Calcula o valor total (quantidade * preço)
            # Esse valor NÃO está armazenado no banco, é calculado na hora da consulta
            (e.quantidade_calcas * e.preco_venda) AS preco_venda_total,
            
            e.fornecedor_id,
            
            # Pega o nome da empresa do fornecedor
            f.nome_empresa
        FROM estoque e
        
        # Faz o JOIN entre estoque e fornecedor usando a chave estrangeira
        JOIN fornecedor f ON e.fornecedor_id = f.id
    """)

    # fetchall() retorna todos os registros encontrados
    dados = cursor.fetchall()
    
    # fecha a conexão com o banco
    db.close()

    # retorna os dados
    return dados