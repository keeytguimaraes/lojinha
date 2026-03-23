from flask import Blueprint, render_template, request, redirect
from models.vendedor.vendedor_insert import inserir_vendedor
from models.vendedor.vendedor_select import listar_vendedores
from models.vendedor.vendedor_update import atualizar_vendedor
from models.vendedor.vendedor_delete import excluir_vendedor

vendedor_bp = Blueprint("vendedor", __name__)

# 🔹 Tela de CADASTRO
@vendedor_bp.route("/vendedores")
def tela_vendedor():
    return render_template("vendedor/vendedores.html")  # só cadastro

# 🔹 LISTA DE VENDEDORES
@vendedor_bp.route("/lista_vendedores")
def lista_vendedores():
    return render_template("vendedor/lista_vendedores.html",
                           vendedores=listar_vendedores())

# 🔹 Inserir vendedor
@vendedor_bp.route("/add_vendedor", methods=["POST"])
def add_vendedor():
    inserir_vendedor(
        request.form["nome"],
        request.form["cpf"],
        request.form["quantidade_vendas"]
    )
    return redirect("/lista_vendedores")  # 👈 VOLTA PRA LISTA

# 🔹 Editar vendedor
@vendedor_bp.route("/editar_vendedor/<int:id>")
def editar_vendedor(id):
    vendedor = next((v for v in listar_vendedores() if v["id"] == id), None)
    return render_template("vendedor/editar_vendedor.html", vendedor=vendedor)

# 🔹 Atualizar vendedor
@vendedor_bp.route("/atualizar_vendedor/<int:id>", methods=["POST"])
def atualizar_vendedor_route(id):
    atualizar_vendedor(
        id,
        request.form["nome"],
        request.form["cpf"],
        request.form["quantidade_vendas"]
    )
    return redirect("/lista_vendedores")

# 🔹 Excluir vendedor
@vendedor_bp.route("/excluir_vendedor/<int:id>")
def excluir_vendedor_route(id):
    excluir_vendedor(id)
    return redirect("/lista_vendedores")