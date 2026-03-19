from flask import Blueprint, render_template, request, redirect
import mysql.connector

fornecedor_bp = Blueprint("fornecedor", __name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="lojinhainha"
)

cursor = db.cursor(dictionary=True)


@fornecedor_bp.route("/fornecedores")
def fornecedores():
    return render_template("fornecedores.html")


# ✅ ADD FORNECEDOR CORRIGIDO
@fornecedor_bp.route("/add_fornecedor", methods=["POST"])
def add_fornecedor():

    nome_empresa = request.form['nome_empresa']
    cnpj = request.form['cnpj']
    produto_quantidade = request.form['produto_quantidade']
    preco = request.form['preco']

    rua = request.form['rua']
    bairro = request.form['bairro']
    numero = request.form['numero']
    cidade = request.form['cidade']

    # cria endereço
    cursor.execute(
        "INSERT INTO endereco (rua, bairro, numero, cidade) VALUES (%s,%s,%s,%s)",
        (rua, bairro, numero, cidade)
    )

    endereco_id = cursor.lastrowid

    # cria fornecedor
    cursor.execute(
        """INSERT INTO fornecedor 
        (nome_empresa, cnpj, produto_quantidade, preco, endereco_id) 
        VALUES (%s,%s,%s,%s,%s)""",
        (nome_empresa, cnpj, produto_quantidade, preco, endereco_id)
    )

    db.commit()

    return redirect("/lista_fornecedores")


# ✅ LISTAR FORNECEDORES CORRIGIDO
@fornecedor_bp.route("/lista_fornecedores")
def lista_fornecedores():

    cursor.execute("""
        SELECT f.id, f.nome_empresa, f.cnpj, f.produto_quantidade, f.preco,
        e.rua, e.bairro, e.numero, e.cidade
        FROM fornecedor f
        JOIN endereco e ON f.endereco_id = e.id
    """)

    fornecedores = cursor.fetchall()

    return render_template("lista_fornecedores.html", fornecedores=fornecedores)


# ✅ EXCLUIR FORNECEDOR CORRIGIDO
@fornecedor_bp.route("/excluir_fornecedor/<int:id>")
def excluir_fornecedor(id):

    cursor.execute("SELECT endereco_id FROM fornecedor WHERE id = %s", (id,))
    endereco_id = cursor.fetchone()["endereco_id"]

    cursor.execute("DELETE FROM fornecedor WHERE id = %s", (id,))
    cursor.execute("DELETE FROM endereco WHERE id = %s", (endereco_id,))

    db.commit()

    return redirect("/lista_fornecedores")