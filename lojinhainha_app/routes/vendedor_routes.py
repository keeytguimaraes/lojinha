from flask import Blueprint, render_template, request, redirect
import mysql.connector

vendedor_bp = Blueprint("vendedor", __name__)

# conexão com banco
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="lojinhainha"
)

cursor = db.cursor(dictionary=True)

# abrir página de cadastro
@vendedor_bp.route("/vendedores")
def vendedores():

    return render_template("vendedores.html")


# listar vendedores
@vendedor_bp.route("/lista_vendedores")
def lista_vendedores():

    cursor.execute("SELECT * FROM vendedor")

    vendedores = cursor.fetchall()

    return render_template("lista_vendedores.html", vendedores=vendedores)

@vendedor_bp.route("/add_vendedor", methods=["POST"])
def add_vendedor():

    nome = request.form['nome']
    cpf = request.form['cpf']
    quantidade_vendas = request.form['quantidade_vendas']

    cursor.execute(
        "INSERT INTO vendedor (nome, cpf, quantidade_vendas) VALUES (%s,%s,%s)",
        (nome, cpf, quantidade_vendas)
    )

    db.commit()

    return redirect("/lista_vendedores")

# excluir vendedor
@vendedor_bp.route("/excluir_vendedor/<int:id>")
def excluir_vendedor(id):

    cursor.execute("DELETE FROM vendedor WHERE id = %s", (id,))
    db.commit()

    return redirect("/lista_vendedores")

@vendedor_bp.route("/")
def index():
    return render_template("index.html")