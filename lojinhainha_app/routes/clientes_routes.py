from flask import Blueprint, render_template, request, redirect
from models.cliente_model import inserir_cliente, listar_clientes, excluir_cliente

cliente_bp = Blueprint("cliente", __name__)


@cliente_bp.route("/")
def index():
    return render_template("index.html")


@cliente_bp.route("/cadastro_cliente")
def cadastro_cliente():
    return render_template("cadastro_cliente.html")


@cliente_bp.route("/add_cliente", methods=["POST"])
def add_cliente():

    inserir_cliente(
        request.form["nome"],
        request.form["cpf"],
        request.form["rua"],
        request.form["bairro"],
        request.form["numero"],
        request.form["cidade"]
    )

    return redirect("/clientes")


@cliente_bp.route("/clientes")
def clientes():
    dados = listar_clientes()
    return render_template("clientes.html", clientes=dados)


@cliente_bp.route("/excluir_cliente/<int:id>")
def excluir_cliente_route(id):
    excluir_cliente(id)
    return redirect("/clientes")