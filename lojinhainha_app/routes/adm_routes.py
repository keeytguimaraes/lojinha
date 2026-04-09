from flask import Blueprint, render_template, request, redirect, flash
from routes.auth_routes import login_required
from models.adm.adm_insert import inserir_adm
from models.adm.adm_select import listar_adms, buscar_adm_por_id
from models.adm.adm_update import atualizar_adm
from models.adm.adm_delete import deletar_adm
from models.login_model import registrar_login  # função que cria login e retorna login_id

# Cria o blueprint para ADM
adm_bp = Blueprint("adm", __name__)

# 🔹 LISTAR ADM
@adm_bp.route("/adms")
@login_required
def listar():
    """
    Lista todos os administradores.
    """
    adms = listar_adms()  # Pega todos os ADMs do banco
    return render_template("adm/listar_adm.html", adms=adms)

# 🔹 CADASTRAR ADM
@adm_bp.route("/adms/novo", methods=["GET", "POST"])
@login_required
def cadastrar():
    """
    Formulário para cadastrar novo ADM.
    Recebe dados do HTML:
    - Dados pessoais: nome, cpf, email, data_nascimento
    - Login: login_nome, login_senha
    """

    if request.method == "POST":
        # 1️⃣ Pega os dados do formulário
        nome = request.form.get("nome")
        cpf = request.form.get("cpf")
        email = request.form.get("email")
        data_nascimento = request.form.get("data_nascimento")
        login_nome = request.form.get("login_nome")
        login_senha = request.form.get("login_senha")  # ⚠️ precisa ter o mesmo name no HTML

        # Checagem simples: se algum dado de login não foi preenchido
        if not login_nome or not login_senha:
            flash("Usuário e senha são obrigatórios!")
            return redirect(request.url)

        # 2️⃣ Cria o login na tabela 'login'
        # registrar_login retorna o ID do login recém-criado
        login_id = registrar_login(login_nome, login_senha, tipo_login=1)  # 1 = ADM

        if not login_id:
            # Caso o usuário já exista, registrar_login retorna False
            flash("Usuário já existe! Escolha outro nome de login.")
            return redirect(request.url)

        # 3️⃣ Cria o ADM usando o login_id retornado
        # Agora passamos apenas o login_id, pois já foi criado
        inserir_adm(nome, cpf, email, data_nascimento, login_id)

        flash("Administrador cadastrado com sucesso!")
        return redirect("/adms")

    # Método GET: exibe o formulário
    return render_template("adm/cadastro_adm.html")


# 🔹 EDITAR ADM
@adm_bp.route("/adms/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar(id):
    """
    Edita os dados do ADM. Não altera login.
    """
    if request.method == "POST":
        nome = request.form.get("nome")
        cpf = request.form.get("cpf")
        email = request.form.get("email")
        data_nascimento = request.form.get("data_nascimento")

        atualizar_adm(id, nome, cpf, email, data_nascimento)
        flash("Administrador atualizado com sucesso!")
        return redirect("/adms")

    adm = buscar_adm_por_id(id)
    return render_template("adm/editar_adm.html", adm=adm)


# 🔹 DELETAR ADM
@adm_bp.route("/adms/deletar/<int:id>")
@login_required
def deletar(id):
    """
    Deleta o ADM do banco (não deleta login automaticamente).
    """
    deletar_adm(id)
    flash("Administrador deletado com sucesso!")
    return redirect("/adms")