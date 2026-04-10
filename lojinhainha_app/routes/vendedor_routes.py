from flask import Blueprint, render_template, request, redirect, flash
from models.vendedor.vendedor_insert import inserir_vendedor
from models.vendedor.vendedor_select import listar_vendedores
from models.vendedor.vendedor_update import atualizar_vendedor
from models.vendedor.vendedor_delete import deletar_vendedor
from models.login_model import registrar_login
from routes.auth_routes import login_required, admin_required

# Criando Blueprint para rotas de vendedor
vendedor_bp = Blueprint("vendedor", __name__)

# 🔹 TELA PRINCIPAL DE CADASTRO DE VENDEDOR
@vendedor_bp.route("/vendedores")
@login_required
@admin_required
def tela_vendedor():
    """
    Apenas renderiza a página de cadastro de vendedores.
    """
    return render_template("vendedor/vendedores.html")


# 🔹 LISTA DE VENDEDORES
@vendedor_bp.route("/lista_vendedores")
@login_required
@admin_required
def lista_vendedores_route():
    """
    Mostra todos os vendedores cadastrados na tabela.
    """
    vendedores = listar_vendedores()  # Pega todos os vendedores do banco
    return render_template("vendedor/lista_vendedores.html", vendedores=vendedores)


# 🔹 CADASTRAR NOVO VENDEDOR COM LOGIN
@vendedor_bp.route("/add_vendedor", methods=["POST"])
@login_required
@admin_required
def add_vendedor():
    """
    Recebe os dados do formulário de cadastro e cria:
    1️⃣ Login na tabela login
    2️⃣ Perfil do vendedor na tabela vendedor com login_id
    """
    # Dados do perfil do vendedor
    nome_vendedor = request.form.get("nome")
    cpf = request.form.get("cpf")
    email = request.form.get("email")
    data_nascimento = request.form.get("data_nascimento")

    # Dados de login do vendedor
    login_nome = request.form.get("login_nome")
    login_senha = request.form.get("login_senha")

    # Validação: senha obrigatória
    if not login_senha or not login_senha.strip():
        flash("Senha é obrigatória para cadastro de vendedor!", "error")
        return redirect("/vendedores")

    # Tenta criar login; retorna o ID do login
    login_id = registrar_login(login_nome, login_senha, tipo_login=2)
    if not login_id:
        flash("Nome de usuário já existe!", "error")
        return redirect("/vendedores")

    # Insere o vendedor com a FK login_id
    inserir_vendedor(nome_vendedor, cpf, email, data_nascimento, login_id)
    flash("Vendedor cadastrado com sucesso!", "success")
    return redirect("/lista_vendedores")


# 🔹 EDITAR VENDEDORES
@vendedor_bp.route("/editar_vendedor/<int:id>")
@login_required
@admin_required
def editar_vendedor(id):
    """
    Busca o vendedor pelo ID e envia para a página de edição.
    """
    from database.connection import get_db

    db = get_db()
    cursor = db.cursor(dictionary=True)

    # 🔥 JOIN com login para trazer nome e senha
    cursor.execute("""
        SELECT vendedor.*, login.nome AS login_nome, login.senha AS login_senha
        FROM vendedor
        JOIN login ON vendedor.login_id = login.id
        WHERE vendedor.id = %s
    """, (id,))

    vendedor = cursor.fetchone()

    db.close()

    return render_template("vendedor/editar_vendedor.html", vendedor=vendedor)

# 🔹 ATUALIZAR VENDEDORES
@vendedor_bp.route("/atualizar_vendedor/<int:id>", methods=["POST"])
@login_required
@admin_required
def atualizar_vendedor_route(id):
    """
    Recebe o formulário de edição e atualiza tanto:
    - Dados do vendedor
    - Dados de login (opcional)
    """
    atualizar_vendedor(
        id,
        request.form.get("nome"),
        request.form.get("cpf"),
        request.form.get("email"),
        request.form.get("data_nascimento"),
        login_nome=request.form.get("login_nome"),
        login_senha=request.form.get("login_senha")
    )
    flash("Vendedor atualizado com sucesso!", "success")
    return redirect("/lista_vendedores")


# 🔹 EXCLUIR VENDEDORES
@vendedor_bp.route("/excluir_vendedor/<int:id>")
@login_required
@admin_required
def excluir_vendedor_route(id):
    """
    Exclui vendedor, suas vendas e login associado.
    """
    deletar_vendedor(id)
    flash("Vendedor excluído com sucesso!", "success")
    return redirect("/lista_vendedores")