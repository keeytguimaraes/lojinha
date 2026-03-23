from flask import Blueprint, render_template, request, redirect
from models.estoque.estoque_insert import inserir_estoque
from models.estoque.estoque_select import listar_estoque
from models.estoque.estoque_update import atualizar_estoque
from models.estoque.estoque_delete import excluir_estoque
from models.vendedor.vendedor_select import listar_vendedores

estoque_bp = Blueprint("estoque", __name__)

# Tela cadastro de estoque
@estoque_bp.route("/estoque")
def estoque():
    return render_template("estoque/estoque.html",
     vendedores=listar_vendedores())

# Inserir estoque
@estoque_bp.route("/add_estoque", methods=["POST"])
def add_estoque():
    inserir_estoque(
        request.form["quantidade_calcas"],
        request.form["preco_venda"],
        request.form["vendedor_id"]
    )
    return redirect("/lista_estoque")

# Listar estoque
@estoque_bp.route("/lista_estoque")
def lista_estoque_route():
    return render_template("estoque/lista_estoque.html", estoque=listar_estoque())

# Editar item do estoque
@estoque_bp.route("/editar_estoque/<int:id>")
def editar_estoque(id):
    item = next((e for e in listar_estoque() if e["id"] == id), None)
    return render_template("estoque/editar_estoque.html",
                           item=item,
                           vendedores=listar_vendedores())

# Atualizar estoque
@estoque_bp.route("/atualizar_estoque/<int:id>", methods=["POST"])
def atualizar_estoque_route(id):
    atualizar_estoque(
        id,
        request.form["quantidade_calcas"],
        request.form["preco_venda"],
        request.form["vendedor_id"]
    )
    return redirect("/lista_estoque")

# Excluir estoque
@estoque_bp.route("/excluir_estoque/<int:id>")
def excluir_estoque_route(id):
    excluir_estoque(id)
    return redirect("/lista_estoque")