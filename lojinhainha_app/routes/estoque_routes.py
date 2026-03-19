from flask import Blueprint, render_template, request, redirect
import mysql.connector

estoque_bp = Blueprint("estoque", __name__)

# conexão com banco
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="lojinhainha"
)

cursor = db.cursor(dictionary=True)

# abrir página de cadastro
@estoque_bp.route("/estoque")
def estoque():

    # pegar vendedores
    cursor.execute("SELECT id, nome FROM vendedor")
    vendedores = cursor.fetchall()

    return render_template("estoque.html", vendedores=vendedores)


# adicionar estoque
@estoque_bp.route("/add_estoque", methods=["POST"])
def add_estoque():

    quantidade = request.form['quantidade_calcas']
    preco = request.form['preco_venda']
    vendedor_id = request.form['vendedor_id']

    cursor.execute(
        "INSERT INTO estoque (quantidade_calcas, preco_venda, vendedor_id) VALUES (%s,%s,%s)",
        (quantidade, preco, vendedor_id)
    )

    db.commit()

    return redirect("/lista_estoque")


# listar estoque
@estoque_bp.route("/lista_estoque")
def lista_estoque():

    cursor.execute("""
    SELECT e.id, e.quantidade_calcas, e.preco_venda, v.nome
    FROM estoque e
    JOIN vendedor v ON e.vendedor_id = v.id
    """)

    estoque = cursor.fetchall()

    return render_template("lista_estoque.html", estoque=estoque)
    
    # excluir produto do estoque
@estoque_bp.route("/excluir_estoque/<int:id>")
def excluir_estoque(id):

    cursor.execute("DELETE FROM estoque WHERE id = %s", (id,))
    db.commit()

    return redirect("/lista_estoque")