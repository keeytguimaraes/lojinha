from flask import Blueprint, render_template, request, redirect, flash
from models.vendedor.vendedor_insert import inserir_vendedor
from models.vendedor.vendedor_select import listar_vendedores
from models.vendedor.vendedor_update import atualizar_vendedor
from models.vendedor.vendedor_delete import excluir_vendedor
from models.login_model import registrar_login
from routes.auth_routes import login_required, admin_required

vendedor_bp = Blueprint("vendedor", __name__)

# 🔹 Tela de CADASTRO
@vendedor_bp.route("/vendedores")
@login_required
@admin_required
def tela_vendedor():
    return render_template("vendedor/vendedores.html")

# 🔹 LISTA DE VENDEDORES
@vendedor_bp.route("/lista_vendedores")
@login_required
@admin_required
def lista_vendedores():
    return render_template(
        "vendedor/lista_vendedores.html",
        vendedores=listar_vendedores()
    )

# 🔹 Inserir vendedor com login e senha
@vendedor_bp.route("/add_vendedor", methods=["POST"])
@login_required
@admin_required
def add_vendedor():
    # Dados do perfil do vendedor
    nome_vendedor = request.form["nome"]
    cpf = request.form["cpf"]
    email = request.form.get("email")
    data_nascimento = request.form.get("data_nascimento")

    # Dados do login do vendedor
    login_nome = request.form["login_nome"]
    login_senha = request.form["login_senha"]

    # Salva login primeiro (tipo_login=2 para VENDEDOR)
    login_id = registrar_login(login_nome, login_senha, tipo_login=2)
    if not login_id:
        flash("Nome de usuário já existe!", "error")
        return redirect("/vendedores")

    # Salva perfil do vendedor no banco (usando seu insert original)
    inserir_vendedor(nome_vendedor, cpf, email, data_nascimento, login_id)

    flash("Vendedor cadastrado com sucesso!", "success")
    return redirect("/lista_vendedores")

# 🔹 Editar vendedor
@vendedor_bp.route("/editar_vendedor/<int:id>")
@login_required
@admin_required
def editar_vendedor(id):
    vendedor = next((v for v in listar_vendedores() if v["id"] == id), None)
    return render_template("vendedor/editar_vendedor.html", vendedor=vendedor)

# 🔹 Atualizar vendedor
@vendedor_bp.route("/atualizar_vendedor/<int:id>", methods=["POST"])
@login_required
@admin_required
def atualizar_vendedor_route(id):
    atualizar_vendedor(
        id,
        request.form["nome"],
        request.form["cpf"],
        request.form.get("email"),
        request.form.get("data_nascimento")
    )
    return redirect("/lista_vendedores")

# 🔹 Excluir vendedor
@vendedor_bp.route("/excluir_vendedor/<int:id>")
@login_required
@admin_required
def excluir_vendedor_route(id):
    excluir_vendedor(id)
    return redirect("/lista_vendedores")