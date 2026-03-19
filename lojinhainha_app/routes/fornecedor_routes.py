from flask import Blueprint, render_template, request, redirect
from models.fornecedor_model import (
    inserir_fornecedor,
    listar_fornecedores,
    excluir_fornecedor
)

fornecedor_bp = Blueprint("fornecedor", __name__)


@fornecedor_bp.route("/fornecedores")
def fornecedores():
    return render_template("fornecedores.html")


@fornecedor_bp.route("/add_fornecedor", methods=["POST"])
def add_fornecedor():

    inserir_fornecedor(
        request.form['nome_empresa'],
        request.form['cnpj'],
        request.form['produto_quantidade'],
        request.form['preco'],
        request.form['rua'],
        request.form['bairro'],
        request.form['numero'],
        request.form['cidade']
    )

    return redirect("/lista_fornecedores")


@fornecedor_bp.route("/lista_fornecedores")
def lista_fornecedores():

    dados = listar_fornecedores()
    return render_template("lista_fornecedores.html", fornecedores=dados)


@fornecedor_bp.route("/excluir_fornecedor/<int:id>")
def excluir_fornecedor_route(id):

    excluir_fornecedor(id)  # CHAMA O MODEL

    return redirect("/lista_fornecedores")