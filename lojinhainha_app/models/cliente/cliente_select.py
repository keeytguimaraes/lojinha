# Importa a função responsável por conectar ao banco de dados
from database.connection import get_db

# Função para listar todos os clientes junto com seus endereços
def listar_clientes():
    
    # conecta no banco
    db = get_db()
    
    # cria o cursor com retorno em formato de dicionário
    # Isso facilita o uso dos dados depois (ex: templates HTML)
    cursor = db.cursor(dictionary=True)

    # busca clientes com endereço
    # Aqui usamos JOIN para unir as tabelas cliente e endereco
    cursor.execute("""
        SELECT 
            c.id,
            c.nome,
            c.cpf,
            c.email,
            c.data_nascimento,
            e.rua,
            e.bairro,
            e.numero,
            e.cidade,
            e.complemento
        FROM cliente c
        JOIN endereco e ON c.endereco_id = e.id
    """)

    # fetchall() retorna todos os registros encontrados
    # Como usamos dictionary=True, será uma lista de dicionários
    dados = cursor.fetchall()
    
    # fecha conexão com o banco
    db.close()

    # retorna os dados
    return dados