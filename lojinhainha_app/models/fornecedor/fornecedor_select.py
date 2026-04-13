# Importa a função responsável por conectar ao banco de dados
from database.connection import get_db

# Função para listar todos os fornecedores com seus respectivos endereços
def listar_fornecedores():
    
    # conecta no banco
    db = get_db()
    
    # cria o cursor com retorno em formato de dicionário
    # Isso permite acessar os dados pelo nome das colunas
    cursor = db.cursor(dictionary=True)

    # busca fornecedores com endereço
    # Utiliza JOIN para unir as tabelas fornecedor e endereco
    cursor.execute("""
        SELECT 
    f.id, 
    f.nome_empresa, 
    f.cnpj, 
    f.produto_quantidade, 
    f.preco,
    f.preco_total,
    e.rua, 
    e.bairro, 
    e.numero, 
    e.cidade,
    e.complemento
FROM fornecedor f
JOIN endereco e ON f.endereco_id = e.id
    """)

    # fetchall() retorna todos os registros encontrados
    # Como usamos dictionary=True, o retorno será uma lista de dicionários
    dados = cursor.fetchall()
    
    # fecha a conexão com o banco
    db.close()

    # retorna os dados
    return dados