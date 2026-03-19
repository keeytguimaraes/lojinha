from flask import Blueprint, render_template, request, redirect
from models.vendas_model import (
    listar_clientes,
    listar_vendedores,
    inserir_venda,
    listar_vendas,
    excluir_venda
)

vendas_bp = Blueprint("vendas", __name__)


@vendas_bp.route("/vendas")
def vendas():

    clientes = listar_clientes()
    vendedores = listar_vendedores()

    return render_template("vendas.html", clientes=clientes, vendedores=vendedores)


@vendas_bp.route("/add_venda", methods=["POST"])
def add_venda():

    inserir_venda(
        request.form["cliente_id"],
        request.form["vendedor_id"],
        request.form["quantidade_vendas"],
        request.form["cpf"],
        request.form["preco"],
        request.form["data"]
    )

    return redirect("/lista_vendas")


@vendas_bp.route("/lista_vendas")
def lista_vendas():

    dados = listar_vendas()
    return render_template("lista_vendas.html", vendas=dados)


@vendas_bp.route("/excluir_venda/<int:id>")
def excluir_venda_route(id):

    excluir_venda(id)  # chama o model

    return redirect("/lista_vendas")