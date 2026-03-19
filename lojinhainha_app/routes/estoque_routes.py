from flask import Blueprint, render_template, request, redirect
from models.estoque_model import (
    listar_vendedores,
    inserir_estoque,
    listar_estoque,
    excluir_estoque
)

estoque_bp = Blueprint("estoque", __name__)


@estoque_bp.route("/estoque")
def estoque():
    vendedores = listar_vendedores()
    return render_template("estoque.html", vendedores=vendedores)


@estoque_bp.route("/add_estoque", methods=["POST"])
def add_estoque():

    inserir_estoque(
        request.form['quantidade_calcas'],
        request.form['preco_venda'],
        request.form['vendedor_id']
    )

    return redirect("/lista_estoque")


@estoque_bp.route("/lista_estoque")
def lista():
    dados = listar_estoque()
    return render_template("lista_estoque.html", estoque=dados)


@estoque_bp.route("/excluir_estoque/<int:id>")
def excluir_estoque_route(id):

    excluir_estoque(id)  # CHAMA O MODEL

    return redirect("/lista_estoque")