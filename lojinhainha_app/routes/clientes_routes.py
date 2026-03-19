from flask import Blueprint, render_template, request, redirect
import mysql.connector

cliente_bp = Blueprint("cliente", __name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="lojinhainha"
)

cursor = db.cursor(dictionary=True)


@cliente_bp.route("/")
def index():
    return render_template("index.html")


@cliente_bp.route("/cadastro_cliente")
def cadastro_cliente():
    return render_template("cadastro_cliente.html")


# ✅ ADD CLIENTE CORRIGIDO
@cliente_bp.route("/add_cliente", methods=["POST"])
def add_cliente():

    nome = request.form["nome"]
    cpf = request.form["cpf"]

    rua = request.form["rua"]
    bairro = request.form["bairro"]
    numero = request.form["numero"]
    cidade = request.form["cidade"]

    # cria endereço primeiro
    cursor.execute(
        "INSERT INTO endereco (rua, bairro, numero, cidade) VALUES (%s,%s,%s,%s)",
        (rua, bairro, numero, cidade)
    )

    endereco_id = cursor.lastrowid

    # cria cliente com FK
    cursor.execute(
        "INSERT INTO cliente (nome, cpf, endereco_id) VALUES (%s,%s,%s)",
        (nome, cpf, endereco_id)
    )

    db.commit()

    return redirect("/clientes")


# ✅ LISTAR CLIENTES CORRIGIDO
@cliente_bp.route("/clientes")
def listar_clientes():

    cursor.execute("""
        SELECT 
            c.id,
            c.nome,
            c.cpf,
            e.rua,
            e.bairro,
            e.numero,
            e.cidade
        FROM cliente c
        JOIN endereco e ON c.endereco_id = e.id
    """)

    clientes = cursor.fetchall()

    return render_template("clientes.html", clientes=clientes)


# ✅ EXCLUIR CLIENTE CORRIGIDO
@cliente_bp.route("/excluir_cliente/<int:id>")
def excluir_cliente(id):

    cursor.execute("SELECT endereco_id FROM cliente WHERE id = %s", (id,))
    endereco_id = cursor.fetchone()["endereco_id"]

    cursor.execute("DELETE FROM cliente WHERE id = %s", (id,))
    cursor.execute("DELETE FROM endereco WHERE id = %s", (endereco_id,))

    db.commit()

    return redirect("/clientes")