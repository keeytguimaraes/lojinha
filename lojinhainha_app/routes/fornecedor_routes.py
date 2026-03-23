from flask import Blueprint, render_template, request, redirect
from models.fornecedor.fornecedor_insert import inserir_fornecedor
from models.fornecedor.fornecedor_select import listar_fornecedores
from models.fornecedor.fornecedor_update import atualizar_fornecedor
from models.fornecedor.fornecedor_delete import excluir_fornecedor

fornecedor_bp = Blueprint("fornecedor", __name__)

# Tela cadastro fornecedor
@fornecedor_bp.route("/fornecedores")
def fornecedores():
    return render_template("fornecedor/fornecedores.html")

# Inserir fornecedor
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

# Listar fornecedores
@fornecedor_bp.route("/lista_fornecedores")
def lista_fornecedores():
    return render_template("fornecedor/lista_fornecedores.html",
                           fornecedores=listar_fornecedores())

# Excluir fornecedor
@fornecedor_bp.route("/excluir_fornecedor/<int:id>")
def excluir_fornecedor_route(id):
    excluir_fornecedor(id)
    return redirect("/lista_fornecedores")

# Editar fornecedor
@fornecedor_bp.route("/editar_fornecedor/<int:id>")
def editar_fornecedor(id):
    fornecedor = next((f for f in listar_fornecedores() if f["id"] == id), None)
    return render_template("fornecedor/editar_fornecedor.html", fornecedor=fornecedor)

# Atualizar fornecedor
@fornecedor_bp.route("/atualizar_fornecedor/<int:id>", methods=["POST"])
def atualizar_fornecedor_route(id):
    atualizar_fornecedor(
        id,
        request.form["nome_empresa"],
        request.form["cnpj"],
        request.form["produto_quantidade"],
        request.form["preco"]
    )
    return redirect("/lista_fornecedores")