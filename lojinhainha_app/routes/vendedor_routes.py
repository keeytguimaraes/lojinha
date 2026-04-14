# Importa recursos do Flask:
# Blueprint → permite organizar rotas em módulos separados (ex: vendedor, cliente, etc)
# render_template → renderiza páginas HTML e envia dados para elas
# request → acessa dados enviados pelo usuário (formulários)
# redirect → redireciona o usuário após ações
# flash → envia mensagens temporárias para o frontend (ex: sucesso/erro)
from flask import Blueprint, render_template, request, redirect, flash

# Importa funções de CRUD do vendedor (camada de model)
# Essas funções fazem comunicação direta com o banco de dados
from models.vendedor.vendedor_insert import inserir_vendedor   # CREATE → inserir vendedor
from models.vendedor.vendedor_select import listar_vendedores  # READ → listar vendedores
from models.vendedor.vendedor_update import atualizar_vendedor # UPDATE → atualizar vendedor
from models.vendedor.vendedor_delete import deletar_vendedor   # DELETE → excluir vendedor

# Importa função que cria login (tabela login)
# Essa função retorna o ID do login criado ou False se já existir
from models.login_model import registrar_login

# Importa decorators de segurança (login e permissão de ADM)
# login_required → exige que o usuário esteja logado
# admin_required → exige que o usuário seja administrador (tipo_login = 1)
from routes.auth_routes import login_required, admin_required

# Criando Blueprint para rotas de vendedor
# "vendedor" → nome interno usado pelo Flask
# __name__ → referência do arquivo atual
vendedor_bp = Blueprint("vendedor", __name__)


# =========================
# TELA PRINCIPAL DE CADASTRO DE VENDEDOR
# =========================
@vendedor_bp.route("/vendedores")  # Define a URL /vendedores
@login_required                    # Só usuários logados podem acessar
@admin_required                    # Apenas administradores podem acessar
def tela_vendedor():
    """
    Apenas renderiza a página de cadastro de vendedores.
    """
    # Renderiza o HTML com formulário de cadastro
    return render_template("vendedor/vendedores.html")


# =========================
# LISTA DE VENDEDORES
# =========================
@vendedor_bp.route("/lista_vendedores")  # URL para listar vendedores
@login_required                          # Protege a rota
@admin_required                          # Apenas ADM pode acessar
def lista_vendedores_route():
    """
    Mostra todos os vendedores cadastrados na tabela.
    """
    
    # Busca todos os vendedores no banco de dados
    vendedores = listar_vendedores()
    
    # Renderiza a página HTML passando a lista de vendedores
    return render_template(
        "vendedor/lista_vendedores.html",
        vendedores=vendedores
    )


# =========================
# CADASTRAR NOVO VENDEDOR COM LOGIN
# =========================
@vendedor_bp.route("/add_vendedor", methods=["POST"])  # Recebe dados via POST
@login_required
@admin_required
def add_vendedor():
    """
    Recebe os dados do formulário e realiza duas operações:
    1️⃣ Cria login na tabela 'login'
    2️⃣ Cria vendedor na tabela 'vendedor' com login_id (FK)
    """

    # =========================
    # DADOS DO VENDEDOR
    # =========================
    # request.form.get("campo") → retorna None se não existir (mais seguro que [])
    nome_vendedor = request.form.get("nome")
    cpf = request.form.get("cpf")
    email = request.form.get("email")
    data_nascimento = request.form.get("data_nascimento")

    # =========================
    # DADOS DE LOGIN
    # =========================
    login_nome = request.form.get("login_nome")
    login_senha = request.form.get("login_senha")

    # =========================
    # VALIDAÇÃO DE SENHA
    # =========================
    # strip() remove espaços antes/depois (evita senha vazia com espaços)
    if not login_senha or not login_senha.strip():
        flash("Senha é obrigatória para cadastro de vendedor!", "error")
        return redirect("/vendedores")

    # =========================
    # CRIAR LOGIN
    # =========================
    # tipo_login=2 → define como vendedor
    login_id = registrar_login(login_nome, login_senha, tipo_login=2)

    # Se login_id for False → usuário já existe
    if not login_id:
        flash("Nome de usuário já existe!", "error")
        return redirect("/vendedores")

    # =========================
    # INSERIR VENDEDOR
    # =========================
    # Cria o vendedor vinculando ao login via chave estrangeira
    inserir_vendedor(nome_vendedor, cpf, email, data_nascimento, login_id)

    # Mensagem de sucesso
    flash("Vendedor cadastrado com sucesso!", "success")

    # Redireciona para a lista de vendedores
    return redirect("/lista_vendedores")


# =========================
# EDITAR VENDEDOR
# =========================
@vendedor_bp.route("/editar_vendedor/<int:id>")  # Recebe ID pela URL
@login_required
@admin_required
def editar_vendedor(id):
    """
    Busca o vendedor no banco com JOIN na tabela login
    para trazer dados completos (perfil + login).
    """

    # Importação interna da função de conexão com banco
    # (feito aqui para evitar dependência global desnecessária)
    from database.connection import get_db

    # Abre conexão com banco de dados
    db = get_db()
    
    # Cria cursor com retorno em formato dicionário (coluna: valor)
    cursor = db.cursor(dictionary=True)

    # =========================
    # QUERY SQL COM JOIN
    # =========================
    # Junta tabela vendedor com tabela login
    # Permite acessar dados do login (nome e senha) junto com vendedor
    cursor.execute("""
        SELECT vendedor.*, login.nome AS login_nome, login.senha AS login_senha
        FROM vendedor
        JOIN login ON vendedor.login_id = login.id
        WHERE vendedor.id = %s
    """, (id,))  # (%s) evita SQL Injection (parâmetro seguro)

    # Busca apenas um resultado (um vendedor específico)
    vendedor = cursor.fetchone()

    # Fecha conexão com banco
    db.close()

    # Renderiza a página de edição com os dados preenchidos
    return render_template(
        "vendedor/editar_vendedor.html",
        vendedor=vendedor
    )


# =========================
# ATUALIZAR VENDEDOR
# =========================
@vendedor_bp.route("/atualizar_vendedor/<int:id>", methods=["POST"])
@login_required
@admin_required
def atualizar_vendedor_route(id):
    """
    Atualiza:
    - Dados do vendedor
    - Dados de login (se fornecidos)
    """

    # Chama função que faz atualização no banco
    atualizar_vendedor(
        id,
        request.form.get("nome"),
        request.form.get("cpf"),
        request.form.get("email"),
        request.form.get("data_nascimento"),
        login_nome=request.form.get("login_nome"),   # pode não vir
        login_senha=request.form.get("login_senha")  # pode não vir
    )

    # Mensagem de sucesso
    flash("Vendedor atualizado com sucesso!", "success")

    # Redireciona para listagem
    return redirect("/lista_vendedores")


# =========================
# EXCLUIR VENDEDOR
# =========================
@vendedor_bp.route("/excluir_vendedor/<int:id>")
@login_required
@admin_required
def excluir_vendedor_route(id):
    """
    Exclui completamente um vendedor:
    - Remove vendas associadas
    - Remove o registro do vendedor
    - Remove o login vinculado
    """

    # Chama função que realiza todas as exclusões no banco
    deletar_vendedor(id)

    # Mensagem de sucesso
    flash("Vendedor excluído com sucesso!", "success")

    # Redireciona para listagem
    return redirect("/lista_vendedores")