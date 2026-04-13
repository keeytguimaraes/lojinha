# Importa recursos do Flask
from flask import Blueprint, render_template, request, redirect, flash

# Importa decorator de autenticação (protege rotas)
from routes.auth_routes import login_required

# Importa funções de CRUD do ADM
from models.adm.adm_insert import inserir_adm
from models.adm.adm_select import listar_adms, buscar_adm_por_id
from models.adm.adm_update import atualizar_adm
from models.adm.adm_delete import deletar_adm

# Importa função para criar login (retorna login_id)
from models.login_model import registrar_login

# Cria o blueprint para ADM (organização modular das rotas)
adm_bp = Blueprint("adm", __name__)

#  LISTAR ADM
@adm_bp.route("/adms")
@login_required  # exige que o usuário esteja logado
def listar():
    """
    Lista todos os administradores.
    """
    
    # Busca todos os ADMs no banco
    adms = listar_adms()
    
    # Renderiza o HTML passando a lista
    return render_template("adm/listar_adm.html", adms=adms)


#  CADASTRAR ADM
@adm_bp.route("/adms/novo", methods=["GET", "POST"])
@login_required
def cadastrar():
    """
    Formulário para cadastrar novo ADM.
    Recebe dados do HTML:
    - Dados pessoais: nome, cpf, email, data_nascimento
    - Login: login_nome, login_senha
    """

    # Se o formulário foi enviado
    if request.method == "POST":
        
        # 1️⃣ Pega os dados do formulário (request.form)
        nome = request.form.get("nome")
        cpf = request.form.get("cpf")
        email = request.form.get("email")
        data_nascimento = request.form.get("data_nascimento")
        login_nome = request.form.get("login_nome")
        login_senha = request.form.get("login_senha")  # deve bater com o name do HTML

        # Validação simples: login e senha obrigatórios
        if not login_nome or not login_senha:
            flash("Usuário e senha são obrigatórios!")
            return redirect(request.url)

        # 2️⃣ Cria o login na tabela 'login'
        # Retorna o ID do login criado
        login_id = registrar_login(login_nome, login_senha, tipo_login=1)  # 1 = ADM

        # Se já existir usuário com esse nome
        if not login_id:
            flash("Usuário já existe! Escolha outro nome de login.")
            return redirect(request.url)

        # 3️⃣ Cria o ADM com o login_id
        inserir_adm(nome, cpf, email, data_nascimento, login_id)

        # Mensagem de sucesso
        flash("Administrador cadastrado com sucesso!")
        
        # Redireciona para listagem
        return redirect("/adms")

    # Método GET → apenas exibe o formulário
    return render_template("adm/cadastro_adm.html")


#  EDITAR ADM
@adm_bp.route("/adms/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar(id):
    """
    Edita os dados do ADM. Não altera login.
    """

    # Se enviou formulário (POST)
    if request.method == "POST":
        
        # Pega os dados atualizados
        nome = request.form.get("nome")
        cpf = request.form.get("cpf")
        email = request.form.get("email")
        data_nascimento = request.form.get("data_nascimento")

        # Atualiza no banco
        atualizar_adm(id, nome, cpf, email, data_nascimento)

        # Feedback para o usuário
        flash("Administrador atualizado com sucesso!")
        
        # Redireciona para listagem
        return redirect("/adms")

    # Método GET → busca dados do ADM para preencher o formulário
    adm = buscar_adm_por_id(id)
    
    # Renderiza página de edição com dados preenchidos
    return render_template("adm/editar_adm.html", adm=adm)


#  DELETAR ADM
@adm_bp.route("/adms/deletar/<int:id>")
@login_required
def deletar(id):
    """
    Deleta o ADM do banco (não deleta login automaticamente).
    """

    # Chama função que remove o ADM do banco
    deletar_adm(id)

    # Mensagem de sucesso
    flash("Administrador deletado com sucesso!")
    
    # Redireciona para listagem
    return redirect("/adms")