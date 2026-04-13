# Importa a função responsável por conectar ao banco de dados
from database.connection import get_db

# Função para listar todas as vendas com informações de cliente e vendedor
def listar_vendas():
    
    # Cria a conexão com o banco de dados
    db = get_db()
    
    # Cria o cursor com retorno em formato de dicionário
    # Isso permite acessar os dados pelo nome das colunas
    cursor = db.cursor(dictionary=True)

    # Executa a consulta SQL para buscar as vendas
    # Utiliza JOIN para relacionar vendas com cliente e vendedor
    cursor.execute("""
        SELECT 
    v.id,
    c.nome AS cliente,
    ve.nome AS vendedor,
    v.quantidade_vendas,
    v.preco,
    v.preco_total,
    v.data
    FROM vendas v
    JOIN cliente c ON v.cliente_id = c.id
    JOIN login ve ON v.vendedor_id = ve.id;
    """)

    # fetchall() retorna todos os registros encontrados
    dados = cursor.fetchall()
    
    # Fecha a conexão com o banco
    db.close()

    # Retorna os dados
    return dados