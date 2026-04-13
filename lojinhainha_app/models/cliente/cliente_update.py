# Importa a função responsável por conectar ao banco de dados
from database.connection import get_db

# Função para atualizar um cliente e seu endereço
def atualizar_cliente(id, nome, cpf, email, data_nascimento, rua, bairro, numero, cidade, complemento):
    
    # conecta no banco
    db = get_db()
    
    # cria o cursor para executar comandos SQL
    cursor = db.cursor()

    # atualiza dados do cliente
    # Atualiza os dados principais na tabela cliente
    cursor.execute(
        """
        UPDATE cliente 
        SET nome=%s, cpf=%s, email=%s, data_nascimento=%s 
        WHERE id=%s
        """,
        (nome, cpf, email, data_nascimento, id)
    )

    # pega id do endereço relacionado
    # Busca o endereco_id associado ao cliente
    cursor.execute("SELECT endereco_id FROM cliente WHERE id = %s", (id,))
    
    # fetchone() retorna uma tupla → [0] pega o valor do endereco_id
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

    # Confirma todas as alterações feitas no banco
    db.commit()
    
    # Fecha a conexão com o banco
    db.close()