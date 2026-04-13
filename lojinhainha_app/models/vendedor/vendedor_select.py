# Importa a função responsável por conectar ao banco de dados
from database.connection import get_db

# Função para listar todos os vendedores com seus dados de login
def listar_vendedores():
    """
    Lista todos os vendedores com dados de login.
    """
    
    # Cria a conexão com o banco de dados
    db = get_db()
    
    # Cria o cursor com retorno em formato de dicionário
    # Isso permite acessar os dados pelo nome das colunas
    cursor = db.cursor(dictionary=True)

    # Executa a consulta SQL
    # Busca todos os dados da tabela vendedor (*) e também o nome do login
    cursor.execute("""
    SELECT vendedor.*, login.nome AS login_nome
    FROM vendedor
    
    # Faz o JOIN entre vendedor e login usando a chave estrangeira
    JOIN login ON vendedor.login_id = login.id
    """)

    # fetchall() retorna todos os registros encontrados
    dados = cursor.fetchall()
    
    # Fecha a conexão com o banco
    db.close()
    
    # Retorna os dados
    return dados