# Importa a função responsável por conectar ao banco de dados
from database.connection import get_db

# Função para atualizar um fornecedor e seu endereço
def atualizar_fornecedor(id, nome, cnpj, quantidade, preco, rua, bairro, numero, cidade, complemento):
    
    # conecta no banco
    db = get_db()
    
    # cria o cursor para executar comandos SQL
    cursor = db.cursor()

    # Converte a quantidade para inteiro
    quantidade = int(quantidade)
    
    # Converte o preço para float
    # O replace(",", ".") permite aceitar valores no formato brasileiro (ex: 10,50)
    preco = float(preco.replace(",", "."))  
    
    # Calcula o preço total (quantidade * preço)
    preco_total = quantidade * preco

    # atualiza fornecedor
    # Atualiza os dados principais do fornecedor na tabela fornecedor
    cursor.execute(
        """UPDATE fornecedor 
        SET nome_empresa=%s, cnpj=%s, produto_quantidade=%s, preco=%s, preco_total=%s 
        WHERE id=%s""",
        (nome, cnpj, quantidade, preco, preco_total, id)
    )

    # pega id do endereço relacionado
    # Busca o endereco_id associado ao fornecedor
    cursor.execute("SELECT endereco_id FROM fornecedor WHERE id = %s", (id,))
    
    # fetchone() retorna uma tupla → [0] acessa o valor do endereco_id
    endereco_id = cursor.fetchone()[0]

    # atualiza endereço
    # Atualiza os dados do endereço na tabela endereco
    cursor.execute(
        """
        UPDATE endereco 
        SET rua=%s, bairro=%s, numero=%s, cidade=%s, complemento=%s 
        WHERE id=%s
        """,
        (rua, bairro, numero, cidade, complemento, endereco_id)
    )

    # Confirma todas as alterações no banco
    db.commit()
    
    # Fecha a conexão com o banco
    db.close()