from flask import Blueprint, render_template, request, redirect
from models.vendas.vendas_insert import inserir_venda
from models.vendas.vendas_select import listar_vendas
from models.vendas.vendas_update import atualizar_venda
from models.vendas.vendas_delete import excluir_venda
from models.cliente.cliente_select import listar_clientes
from models.vendedor.vendedor_select import listar_vendedores

vendas_bp = Blueprint("vendas", __name__)

# Tela cadastro de vendas
@vendas_bp.route("/vendas")
def vendas():
    return render_template("vendas/vendas.html",
     clientes=listar_clientes(),
     vendedores=listar_vendedores())

# Inserir venda
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

# Listar vendas
@vendas_bp.route("/lista_vendas")
def lista_vendas_route():
    return render_template("vendas/lista_vendas.html", vendas=listar_vendas())

# Excluir venda
@vendas_bp.route("/excluir_venda/<int:id>")
def excluir_venda_route(id):
    excluir_venda(id)
    return redirect("/lista_vendas")

# Editar venda
@vendas_bp.route("/editar_venda/<int:id>")
def editar_venda(id):
    venda = next((v for v in listar_vendas() if v["id"] == id), None)
    return render_template("vendas/editar_venda.html", venda=venda)

# Atualizar venda
@vendas_bp.route("/atualizar_venda/<int:id>", methods=["POST"])
def atualizar_venda_route(id):
    atualizar_venda(
        id,
        request.form["quantidade_vendas"],
        request.form["preco"]
    )
    return redirect("/lista_vendas")