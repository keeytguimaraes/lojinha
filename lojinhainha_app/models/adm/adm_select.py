# Importa a função responsável por criar conexão com o banco de dados
from database.connection import get_db

# Função que lista todos os administradores
def listar_adms():
    #Lista todos os administradores com dados de login.

    # Cria a conexão com o banco
    db = get_db()
    
    # Cria o cursor com dictionary=True
    # Isso faz com que os resultados venham como dicionário (ex: {"nome": "João"})
    # em vez de tuplas (ex: ("João",))
    cursor = db.cursor(dictionary=True)

    # Executa uma consulta SQL com JOIN
    # Aqui estamos juntando duas tabelas:
    # adm (administradores) e login (dados de login)
    cursor.execute("""
        SELECT 
            a.id, a.nome, a.cpf, a.email, a.data_nascimento,
            l.nome AS login_nome
        FROM adm a
        JOIN login l ON a.login_id = l.id
    """)

    # fetchall() pega TODOS os resultados da consulta
    # Como usamos dictionary=True, será uma lista de dicionários
    dados = cursor.fetchall()
    
    # Fecha a conexão com o banco
    db.close()
    
    # Retorna os dados encontrados
    return dados


# Função que busca um administrador específico pelo ID
def buscar_adm_por_id(id):
    #Busca um administrador pelo ID.
    
    # Cria conexão com o banco
    db = get_db()
    
    # Cursor com retorno em formato de dicionário
    cursor = db.cursor(dictionary=True)

    # Executa a consulta SQL para buscar um único administrador
    # WHERE id = %s garante que só traga o ADM com o ID informado
    # (id,) é uma tupla → evita SQL Injection
    cursor.execute(
        "SELECT * FROM adm WHERE id = %s",
        (id,)
    )

    # fetchone() pega apenas UM resultado (ou None se não encontrar)
    dado = cursor.fetchone()
    
    # Fecha a conexão com o banco
    db.close()
    
    # Retorna o resultado encontrado
    return dado