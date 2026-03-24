from flask import Blueprint, render_template, request, redirect
from models.cliente.cliente_insert import inserir_cliente
from models.cliente.cliente_select import listar_clientes
from models.cliente.cliente_update import atualizar_cliente
from models.cliente.cliente_delete import excluir_cliente

cliente_bp = Blueprint("cliente", __name__)

# Página inicial
@cliente_bp.route("/")
def index():
    return render_template("index.html")

# Tela de cadastro
@cliente_bp.route("/cadastro_cliente")
def cadastro_cliente():
    return render_template("cliente/cadastro_cliente.html")

# Inserir cliente
@cliente_bp.route("/add_cliente", methods=["POST"])
def add_cliente():
    inserir_cliente(
        request.form["nome"],
        request.form["cpf"],
        request.form["rua"],
        request.form["bairro"],
        request.form["numero"],
        request.form["cidade"],
        request.form["complemento"]
    )
    return redirect("/clientes")

# Listar clientes
@cliente_bp.route("/clientes")
def clientes():
    return render_template("cliente/clientes.html", clientes=listar_clientes())

# Excluir cliente
@cliente_bp.route("/excluir_cliente/<int:id>")
def excluir_cliente_route(id):
    excluir_cliente(id)
    return redirect("/clientes")

# Abrir edição
@cliente_bp.route("/editar_cliente/<int:id>")
def editar_cliente(id):
    cliente = next((c for c in listar_clientes() if c["id"] == id), None)
    return render_template("cliente/editar_cliente.html", cliente=cliente)

# Atualizar cliente
@cliente_bp.route("/atualizar_cliente/<int:id>", methods=["POST"])
def atualizar_cliente_route(id):
    atualizar_cliente(
        id,
        request.form["nome"],
        request.form["cpf"],
        request.form["rua"],
        request.form["bairro"],
        request.form["numero"],
        request.form["cidade"]
    )
    return redirect("/clientes")