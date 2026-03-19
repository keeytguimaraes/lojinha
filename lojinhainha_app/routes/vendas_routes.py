from flask import Blueprint, render_template, request, redirect
import mysql.connector

vendas_bp = Blueprint("vendas", __name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="lojinhainha"
)

cursor = db.cursor(dictionary=True)

# abrir página de vendas
@vendas_bp.route("/vendas")
def vendas():

    cursor.execute("SELECT id, nome FROM cliente")
    clientes = cursor.fetchall()

    cursor.execute("SELECT id, nome FROM vendedor")
    vendedores = cursor.fetchall()

    return render_template("vendas.html", clientes=clientes, vendedores=vendedores)


# adicionar venda
@vendas_bp.route("/add_venda", methods=["POST"])
def add_venda():

    cliente_id = request.form["cliente_id"]
    vendedor_id = request.form["vendedor_id"]
    quantidade = request.form["quantidade_vendas"]
    cpf = request.form["cpf"]
    preco = request.form["preco"]
    data = request.form["data"]

    cursor.execute(
        """
        INSERT INTO vendas (vendedor_id, cliente_id, quantidade_vendas, cpf, preco, data)
        VALUES (%s,%s,%s,%s,%s,%s)
        """,
        (vendedor_id, cliente_id, quantidade, cpf, preco, data)
    )

    db.commit()

    return redirect("/lista_vendas")


# listar vendas
@vendas_bp.route("/lista_vendas")
def lista_vendas():

    cursor.execute("""
    SELECT v.id, c.nome AS cliente, ve.nome AS vendedor,
           v.quantidade_vendas, v.preco, v.data
    FROM vendas v
    JOIN cliente c ON v.cliente_id = c.id
    JOIN vendedor ve ON v.vendedor_id = ve.id
    """)

    vendas = cursor.fetchall()

    return render_template("lista_vendas.html", vendas=vendas)

# excluir venda
@vendas_bp.route("/excluir_venda/<int:id>")
def excluir_venda(id):

    cursor.execute("DELETE FROM vendas WHERE id = %s", (id,))
    db.commit()

    return redirect("/lista_vendas")