# Importa recursos do Flask:
# Blueprint → organização de rotas
# render_template → renderizar HTML
# request → acessar dados de formulário
# redirect → redirecionar páginas
# flash → exibir mensagens temporárias (sucesso/erro)
from flask import Blueprint, render_template, request, redirect, flash

# Importa funções de CRUD do vendedor (camada de model)
from models.vendedor.vendedor_insert import inserir_vendedor
from models.vendedor.vendedor_select import listar_vendedores
from models.vendedor.vendedor_update import atualizar_vendedor
from models.vendedor.vendedor_delete import deletar_vendedor

# Importa função que cria login (tabela login)
from models.login_model import registrar_login

# Importa decorators de segurança (login e permissão de ADM)
from routes.auth_routes import login_required, admin_required

# Criando Blueprint para rotas de vendedor
# Isso organiza todas as rotas relacionadas a vendedor
vendedor_bp = Blueprint("vendedor", __name__)

#  TELA PRINCIPAL DE CADASTRO DE VENDEDOR
@vendedor_bp.route("/vendedores")  # Define a URL /vendedores
@login_required                    # Exige usuário logado
@admin_required                   # Exige que seja ADM
def tela_vendedor():
    """
    Apenas renderiza a página de cadastro de vendedores.
    """
    # Renderiza o HTML do formulário de cadastro
    return render_template("vendedor/vendedores.html")


#  LISTA DE VENDEDORES
@vendedor_bp.route("/lista_vendedores")  # URL para listar vendedores
@login_required                          # Protege a rota
@admin_required                          # Apenas ADM pode acessar
def lista_vendedores_route():
    """
    Mostra todos os vendedores cadastrados na tabela.
    """
    vendedores = listar_vendedores()  # Busca todos os vendedores no banco
    # Renderiza a página passando os dados
    return render_template("vendedor/lista_vendedores.html", vendedores=vendedores)


#  CADASTRAR NOVO VENDEDOR COM LOGIN
@vendedor_bp.route("/add_vendedor", methods=["POST"])  # Recebe dados via POST
@login_required
@admin_required
def add_vendedor():
    """
    Recebe os dados do formulário de cadastro e cria:
    1️⃣ Login na tabela login
    2️⃣ Perfil do vendedor na tabela vendedor com login_id
    """

    # Dados do perfil do vendedor (tabela vendedor)
    nome_vendedor = request.form.get("nome")
    cpf = request.form.get("cpf")
    email = request.form.get("email")
    data_nascimento = request.form.get("data_nascimento")

    # Dados de login (tabela login)
    login_nome = request.form.get("login_nome")
    login_senha = request.form.get("login_senha")

    # Validação: senha obrigatória
    # strip() remove espaços em branco
    if not login_senha or not login_senha.strip():
        flash("Senha é obrigatória para cadastro de vendedor!", "error")
        return redirect("/vendedores")

    # Cria login na tabela login
    # tipo_login=2 → vendedor
    login_id = registrar_login(login_nome, login_senha, tipo_login=2)

    # Se retornar False, significa que o nome já existe
    if not login_id:
        flash("Nome de usuário já existe!", "error")
        return redirect("/vendedores")

    # Insere o vendedor na tabela vendedor com a FK login_id
    inserir_vendedor(nome_vendedor, cpf, email, data_nascimento, login_id)

    # Mensagem de sucesso
    flash("Vendedor cadastrado com sucesso!", "success")

    # Redireciona para a lista
    return redirect("/lista_vendedores")


#  EDITAR VENDEDORES
@vendedor_bp.route("/editar_vendedor/<int:id>")  # Recebe ID pela URL
@login_required
@admin_required
def editar_vendedor(id):
    """
    Busca o vendedor pelo ID e envia para a página de edição.
    """

    # Importação interna da conexão com banco
    from database.connection import get_db

    # Abre conexão com banco
    db = get_db()
    cursor = db.cursor(dictionary=True)  # Retorna dados como dicionário

    #  JOIN com login para trazer dados do vendedor + login
    cursor.execute("""
        SELECT vendedor.*, login.nome AS login_nome, login.senha AS login_senha
        FROM vendedor
        JOIN login ON vendedor.login_id = login.id
        WHERE vendedor.id = %s
    """, (id,))

    # Pega o resultado da consulta
    vendedor = cursor.fetchone()

    # Fecha conexão com banco
    db.close()

    # Renderiza a página de edição com os dados preenchidos
    return render_template("vendedor/editar_vendedor.html", vendedor=vendedor)


# ATUALIZAR VENDEDORES
@vendedor_bp.route("/atualizar_vendedor/<int:id>", methods=["POST"])
@login_required
@admin_required
def atualizar_vendedor_route(id):
    """
    Recebe o formulário de edição e atualiza tanto:
    - Dados do vendedor
    - Dados de login (opcional)
    """

    # Chama função que atualiza vendedor e login (se enviado)
    atualizar_vendedor(
        id,
        request.form.get("nome"),
        request.form.get("cpf"),
        request.form.get("email"),
        request.form.get("data_nascimento"),
        login_nome=request.form.get("login_nome"),     # pode ser None
        login_senha=request.form.get("login_senha")    # pode ser None
    )

    # Mensagem de sucesso
    flash("Vendedor atualizado com sucesso!", "success")

    # Redireciona para listagem
    return redirect("/lista_vendedores")


# EXCLUIR VENDEDORES
@vendedor_bp.route("/excluir_vendedor/<int:id>")
@login_required
@admin_required
def excluir_vendedor_route(id):
    """
    Exclui vendedor, suas vendas e login associado.
    """

    # Chama função que:
    # - deleta vendas
    # - deleta vendedor
    # - deleta login
    deletar_vendedor(id)

    # Mensagem de sucesso
    flash("Vendedor excluído com sucesso!", "success")

    # Redireciona para listagem
    return redirect("/lista_vendedores")