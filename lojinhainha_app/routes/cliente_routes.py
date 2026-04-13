# Importa recursos do Flask
from flask import Blueprint, render_template, request, redirect

# Importa decorator de autenticação (protege rotas)
from routes.auth_routes import login_required

# Importa funções de CRUD do cliente
from models.cliente.cliente_insert import inserir_cliente
from models.cliente.cliente_select import listar_clientes
from models.cliente.cliente_update import atualizar_cliente
from models.cliente.cliente_delete import excluir_cliente

# Cria o blueprint para cliente (organização das rotas)
cliente_bp = Blueprint("cliente", __name__)

# Página inicial
@cliente_bp.route("/")
@login_required
def index():
    # Renderiza a página inicial do sistema
    return render_template("index.html")


# Tela de cadastro
@cliente_bp.route("/cadastro_cliente")
@login_required
def cadastro_cliente():
    # Exibe o formulário de cadastro de cliente
    return render_template("cliente/cadastro_cliente.html")


# Inserir cliente
@cliente_bp.route("/add_cliente", methods=["POST"])
@login_required
def add_cliente():
    
    # Chama a função que insere cliente no banco
    # Pegando todos os dados diretamente do formulário HTML
    inserir_cliente(
        request.form["nome"],
        request.form["cpf"],
        request.form["email"],                 # campo adicional
        request.form["data_nascimento"],       # campo adicional
        request.form["rua"],
        request.form["bairro"],
        request.form["numero"],
        request.form["cidade"],
        request.form["complemento"]
    )

    # Redireciona para a lista de clientes
    return redirect("/clientes")


# Listar clientes
@cliente_bp.route("/clientes")
@login_required
def clientes():
    
    # Renderiza a página de listagem
    # Já passa os clientes diretamente para o HTML
    return render_template(
        "cliente/clientes.html",
        clientes=listar_clientes()
    )


# Excluir cliente
@cliente_bp.route("/excluir_cliente/<int:id>")
@login_required
def excluir_cliente_route(id):
    
    # Chama a função que remove o cliente do banco
    excluir_cliente(id)
    
    # Redireciona para a lista
    return redirect("/clientes")


# Abrir edição
@cliente_bp.route("/editar_cliente/<int:id>")
@login_required
def editar_cliente(id):
    
    # Busca o cliente específico na lista de clientes
    # Usa um generator para encontrar pelo ID
    cliente = next((c for c in listar_clientes() if c["id"] == id), None)
    
    # Renderiza a página de edição com os dados preenchidos
    return render_template("cliente/editar_cliente.html", cliente=cliente)


# Atualizar cliente
@cliente_bp.route("/atualizar_cliente/<int:id>", methods=["POST"])
@login_required
def atualizar_cliente_route(id):
    
    # Chama a função que atualiza os dados do cliente
    atualizar_cliente(
        id,
        request.form["nome"],
        request.form["cpf"],
        request.form["email"],                 # campo adicional
        request.form["data_nascimento"],       # campo adicional
        request.form["rua"],
        request.form["bairro"],
        request.form["numero"],
        request.form["cidade"],
        request.form["complemento"]
    )

    # Redireciona para a lista de clientes
    return redirect("/clientes")