import mysql.connector

try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="lojinhainha"
    )
    print("Conectou ao banco com sucesso!")
except mysql.connector.Error as err:
    print("Erro:", err)