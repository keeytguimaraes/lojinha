from flask import Blueprint, render_template, request, redirect
from models.vendedor_model import (
    listar_vendedores,
    inserir_vendedor,
    excluir_vendedor
)

vendedor_bp = Blueprint("vendedor", __name__)


@vendedor_bp.route("/")
def index():
    return render_template("index.html")


@vendedor_bp.route("/vendedores")
def vendedores():
    return render_template("vendedores.html")


@vendedor_bp.route("/lista_vendedores")
def lista_vendedores():

    dados = listar_vendedores()
    return render_template("lista_vendedores.html", vendedores=dados)


@vendedor_bp.route("/add_vendedor", methods=["POST"])
def add_vendedor():

    inserir_vendedor(
        request.form['nome'],
        request.form['cpf'],
        request.form['quantidade_vendas']
    )

    return redirect("/lista_vendedores")


@vendedor_bp.route("/excluir_vendedor/<int:id>")
def excluir_vendedor_route(id):

    excluir_vendedor(id)  # CHAMA O MODEL

    return redirect("/lista_vendedores")