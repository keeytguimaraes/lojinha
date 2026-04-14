# Importa recursos do Flask
# Blueprint → permite organizar rotas em módulos separados
# render_template → renderiza arquivos HTML
# request → acessa dados enviados pelo usuário (formulários)
# redirect → redireciona o usuário para outra rota
# flash → envia mensagens temporárias para o HTML (feedback)
from flask import Blueprint, render_template, request, redirect, flash

# Importa decorator de autenticação (protege rotas)
# Esse decorator verifica se o usuário está logado antes de acessar a rota
from routes.auth_routes import login_required

# Importa funções de CRUD do ADM
# Cada uma dessas funções interage com o banco de dados
from models.adm.adm_insert import inserir_adm          # CREATE → insere um novo ADM
from models.adm.adm_select import listar_adms, buscar_adm_por_id  # READ → busca dados
from models.adm.adm_update import atualizar_adm        # UPDATE → atualiza dados
from models.adm.adm_delete import deletar_adm          # DELETE → remove dados

# Importa função para criar login (retorna login_id)
# Essa função cria um usuário na tabela de login e retorna o ID gerado
from models.login_model import registrar_login

# Cria o blueprint para ADM (organização modular das rotas)
# "adm" → nome interno do módulo
# __name__ → referência do arquivo atual
adm_bp = Blueprint("adm", __name__)


# =========================
# LISTAR ADM
# =========================
@adm_bp.route("/adms")  # Define a rota /adms
@login_required  # exige que o usuário esteja logado
def listar():
    """
    Lista todos os administradores.
    """

    # Busca todos os ADMs no banco de dados
    # Essa função retorna uma lista (ou coleção) de administradores
    adms = listar_adms()
    
    # Renderiza o template HTML "listar_adm.html"
    # Passa a lista de ADMs para o HTML através da variável "adms"
    return render_template("adm/listar_adm.html", adms=adms)


# =========================
# CADASTRAR ADM
# =========================
@adm_bp.route("/adms/novo", methods=["GET", "POST"])  # Aceita GET e POST
@login_required
def cadastrar():
    """
    Formulário para cadastrar novo ADM.
    Recebe dados do HTML:
    - Dados pessoais: nome, cpf, email, data_nascimento
    - Login: login_nome, login_senha
    """

    # Verifica se o formulário foi enviado (requisição POST)
    if request.method == "POST":
        
        # 1️⃣ Captura os dados enviados pelo formulário HTML
        # request.form.get("campo") pega o valor do input com name="campo"
        nome = request.form.get("nome")
        cpf = request.form.get("cpf")
        email = request.form.get("email")
        data_nascimento = request.form.get("data_nascimento")
        login_nome = request.form.get("login_nome")
        login_senha = request.form.get("login_senha")  # deve bater com o name do HTML

        # Validação simples: login e senha são obrigatórios
        # Se algum deles estiver vazio, mostra erro
        if not login_nome or not login_senha:
            flash("Usuário e senha são obrigatórios!")  # mensagem para o usuário
            return redirect(request.url)  # recarrega a mesma página

        # 2️⃣ Cria o login na tabela 'login'
        # tipo_login=1 indica que é um ADM
        # A função retorna o ID do login criado
        login_id = registrar_login(login_nome, login_senha, tipo_login=1)

        # Se login_id for falso (None ou False), significa que já existe usuário
        if not login_id:
            flash("Usuário já existe! Escolha outro nome de login.")
            return redirect(request.url)

        # 3️⃣ Cria o ADM na tabela de administradores
        # Associa o ADM ao login criado através do login_id
        inserir_adm(nome, cpf, email, data_nascimento, login_id)

        # Mensagem de sucesso exibida ao usuário
        flash("Administrador cadastrado com sucesso!")
        
        # Redireciona para a página de listagem de ADMs
        return redirect("/adms")

    # Caso seja GET (acesso normal à página)
    # Apenas exibe o formulário de cadastro
    return render_template("adm/cadastro_adm.html")


# =========================
# EDITAR ADM
# =========================
@adm_bp.route("/adms/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar(id):
    # Edita os dados do ADM. Não altera login.

    # Se o formulário foi enviado (POST)
    if request.method == "POST":
        
        # Captura os dados atualizados do formulário
        nome = request.form.get("nome")
        cpf = request.form.get("cpf")
        email = request.form.get("email")
        data_nascimento = request.form.get("data_nascimento")

        # Atualiza os dados do ADM no banco de dados
        # Usa o ID recebido na URL
        atualizar_adm(id, nome, cpf, email, data_nascimento)

        # Exibe mensagem de sucesso
        flash("Administrador atualizado com sucesso!")
        
        # Redireciona para a lista de ADMs
        return redirect("/adms")

    # Se for GET:
    # Busca os dados do ADM pelo ID para preencher o formulário
    adm = buscar_adm_por_id(id)
    
    # Renderiza a página de edição já com os dados preenchidos
    return render_template("adm/editar_adm.html", adm=adm)


# =========================
# DELETAR ADM
# =========================
@adm_bp.route("/adms/deletar/<int:id>")  # Recebe o ID pela URL
@login_required
def deletar(id):
    # Deleta o ADM do banco (não deleta login automaticamente)

    # Chama função que remove o ADM do banco de dados
    deletar_adm(id)

    # Exibe mensagem de sucesso
    flash("Administrador deletado com sucesso!")
    
    # Redireciona para a listagem de ADMs
    return redirect("/adms")