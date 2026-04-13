# Importa a função responsável por conectar ao banco de dados
from database.connection import get_db

# Função para inserir um cliente junto com seu endereço
def inserir_cliente(nome, cpf, email, data_nascimento, rua, bairro, numero, cidade, complemento):
    
    # cria conexão com banco
    db = get_db()
    
    # cria o cursor para executar comandos SQL
    cursor = db.cursor()

    # insere endereço do cliente
    # Primeiro inserimos o endereço porque o cliente depende dele (FK)
    cursor.execute(
        """
        INSERT INTO endereco (rua, bairro, numero, cidade, complemento) 
        VALUES (%s,%s,%s,%s,%s)
        """,
        (rua, bairro, numero, cidade, complemento)
    )

    # pega id do endereço criado
    # lastrowid retorna o ID do último registro inserido
    # Isso é essencial para relacionar com o cliente depois
    endereco_id = cursor.lastrowid

    # insere cliente com o endereço + novos campos
    # Agora usamos o endereco_id para vincular o cliente ao endereço
    cursor.execute(
        """
        INSERT INTO cliente (nome, cpf, email, data_nascimento, endereco_id) 
        VALUES (%s,%s,%s,%s,%s)
        """,
        (nome, cpf, email, data_nascimento, endereco_id)
    )

    # salva alterações
    # Confirma as duas inserções no banco (endereço + cliente)
    db.commit()
    
    # fecha conexão com o banco
    db.close()