# Importa a função responsável por conectar ao banco de dados
from database.connection import get_db

# Função para atualizar uma venda
def atualizar_venda(id, cliente_id, vendedor_id, quantidade, fornecedor_id):
    
    # Cria a conexão com o banco
    db = get_db()
    
    # Cria o cursor para executar comandos SQL
    cursor = db.cursor()

    # Converte a quantidade para inteiro
    quantidade = int(quantidade)

    # BUSCAR PREÇO DO FORNECEDOR
    # Executa uma consulta para obter o preço do fornecedor com base no ID
    cursor.execute("SELECT preco FROM fornecedor WHERE id = %s", (fornecedor_id,))
    
    # fetchone() retorna uma tupla ou None
    fornecedor = cursor.fetchone()

    # Se o fornecedor existir, pega o preço (posição [0]) e converte para float
    # Caso contrário, define preço como 0 (evita erro)
    preco_fornecedor = float(fornecedor[0]) if fornecedor else 0

    # CALCULAR
    # Aplica um acréscimo de 20% sobre o preço do fornecedor
    preco_unitario = preco_fornecedor * 1.2
    
    # Calcula o preço total com base na quantidade
    preco_total = preco_unitario * quantidade

    # ATUALIZA TUDO
    # Atualiza os dados da venda na tabela vendas
    cursor.execute(
        """UPDATE vendas 
           SET cliente_id=%s, vendedor_id=%s, quantidade_vendas=%s, preco=%s, preco_total=%s 
           WHERE id=%s""",
        (cliente_id, vendedor_id, quantidade, preco_unitario, preco_total, id)
    )

    # Confirma as alterações no banco
    db.commit()
    
    # Fecha a conexão com o banco
    db.close()