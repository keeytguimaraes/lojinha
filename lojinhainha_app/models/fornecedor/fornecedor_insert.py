# Importa a função responsável por conectar ao banco de dados
from database.connection import get_db

# Função para inserir um fornecedor com endereço e dados de produto
def inserir_fornecedor(nome_empresa, cnpj, produto_quantidade, preco, rua, bairro, numero, cidade, complemento):
    
    # conecta no banco
    db = get_db()
    
    # cria o cursor para executar comandos SQL
    cursor = db.cursor()

    # cria endereço
    # Executa a inserção de um novo endereço na tabela endereco
    # Os valores (rua, bairro, numero, cidade, complemento) são passados
    # como parâmetros para evitar SQL Injection e garantir segurança
    # Essa operação adiciona o endereço ao banco para posteriormente
    # ser associado ao fornecedor
    cursor.execute(
        cursor.execute(
    "INSERT INTO endereco (rua, bairro, numero, cidade, complemento) VALUES (%s,%s,%s,%s,%s)",
    (rua, bairro, numero, cidade, complemento)
)
    )

    # pega o ID do último registro inserido (endereço)
    endereco_id = cursor.lastrowid

    # Converte quantidade para inteiro
    produto_quantidade = int(produto_quantidade)
    
    # Converte preço para float
    preco = float(preco)

    # Calcula o preço total (quantidade * preço)
    preco_total = produto_quantidade * preco

    # cria fornecedor
    # Insere os dados do fornecedor, incluindo o endereço e o preço total
    cursor.execute(
        """INSERT INTO fornecedor 
        (nome_empresa, cnpj, produto_quantidade, preco, endereco_id, preco_total) 
        VALUES (%s,%s,%s,%s,%s,%s)""",
        (nome_empresa, cnpj, produto_quantidade, preco, endereco_id, preco_total)
    )

    # Confirma as alterações no banco
    db.commit()
    
    # Fecha a conexão
    db.close()