# Importa recursos do Flask
# Blueprint → organiza rotas em módulos separados
# render_template → renderiza HTML
# request → acessa dados enviados pelo usuário (formulários)
# redirect → redireciona o usuário para outra rota
from flask import Blueprint, render_template, request, redirect

# Importa decorator de autenticação (protege rotas)
# Garante que apenas usuários logados acessem essas rotas
from routes.auth_routes import login_required

# Importa funções de CRUD do cliente
# Cada função interage diretamente com o banco de dados
from models.cliente.cliente_insert import inserir_cliente   # CREATE → inserir cliente
from models.cliente.cliente_select import listar_clientes   # READ → listar clientes
from models.cliente.cliente_update import atualizar_cliente # UPDATE → atualizar cliente
from models.cliente.cliente_delete import excluir_cliente   # DELETE → remover cliente

# Cria o blueprint para cliente (organização das rotas)
# "cliente" → nome interno usado no Flask (ex: url_for)
# __name__ → referência do arquivo atual
cliente_bp = Blueprint("cliente", __name__)


# =========================
# PÁGINA INICIAL
# =========================
@cliente_bp.route("/")  # rota raiz desse blueprint
@login_required         # exige que o usuário esteja logado
def index():
    # Renderiza a página inicial do sistema
    return render_template("index.html")


# =========================
# TELA DE CADASTRO
# =========================
@cliente_bp.route("/cadastro_cliente")
@login_required
def cadastro_cliente():
    # Apenas exibe o formulário HTML para cadastrar cliente
    return render_template("cliente/cadastro_cliente.html")


# =========================
# INSERIR CLIENTE
# =========================
@cliente_bp.route("/add_cliente", methods=["POST"])
@login_required
def add_cliente():
    
    # Chama a função que insere cliente no banco
    # Os dados são pegos diretamente do formulário HTML (request.form)
    # request.form["campo"] → acessa o valor do input com name="campo"
    inserir_cliente(
        request.form["nome"],               # nome do cliente
        request.form["cpf"],                # CPF do cliente
        request.form["email"],              # email (campo adicional)
        request.form["data_nascimento"],    # data de nascimento (campo adicional)
        request.form["rua"],                # endereço - rua
        request.form["bairro"],             # endereço - bairro
        request.form["numero"],             # endereço - número
        request.form["cidade"],             # endereço - cidade
        request.form["complemento"]         # endereço - complemento (opcional)
    )

    # Após inserir, redireciona para a página de listagem de clientes
    return redirect("/clientes")


# =========================
# LISTAR CLIENTES
# =========================
@cliente_bp.route("/clientes")
@login_required
def clientes():
    
    # Renderiza a página de listagem de clientes
    # listar_clientes() busca todos os clientes no banco
    # O resultado é passado para o HTML na variável "clientes"
    return render_template(
        "cliente/clientes.html",
        clientes=listar_clientes()
    )


# =========================
# EXCLUIR CLIENTE
# =========================
@cliente_bp.route("/excluir_cliente/<int:id>")
@login_required
def excluir_cliente_route(id):
    
    # Recebe o ID do cliente pela URL
    # Exemplo: /excluir_cliente/5 → id = 5
    
    # Chama a função que remove o cliente do banco
    excluir_cliente(id)
    
    # Redireciona novamente para a lista de clientes
    return redirect("/clientes")


# =========================
# ABRIR TELA DE EDIÇÃO
# =========================
@cliente_bp.route("/editar_cliente/<int:id>")
@login_required
def editar_cliente(id):
    
    # Busca o cliente específico dentro da lista de clientes
    # listar_clientes() retorna todos os clientes
    # next(...) percorre a lista até encontrar o primeiro cliente com ID igual
    # Se não encontrar, retorna None
    cliente = next((c for c in listar_clientes() if c["id"] == id), None)
    
    # Renderiza a tela de edição já com os dados preenchidos
    # O HTML recebe o cliente e preenche os inputs automaticamente
    return render_template("cliente/editar_cliente.html", cliente=cliente)


# =========================
# ATUALIZAR CLIENTE
# =========================
@cliente_bp.route("/atualizar_cliente/<int:id>", methods=["POST"])
@login_required
def atualizar_cliente_route(id):
    
    # Recebe o ID pela URL e os dados atualizados pelo formulário
    
    # Chama a função que atualiza os dados no banco
    atualizar_cliente(
        id,                                 # ID do cliente a ser atualizado
        request.form["nome"],               # novo nome
        request.form["cpf"],                # novo CPF
        request.form["email"],              # novo email
        request.form["data_nascimento"],    # nova data de nascimento
        request.form["rua"],                # novo endereço
        request.form["bairro"],
        request.form["numero"],
        request.form["cidade"],
        request.form["complemento"]
    )

    # Após atualizar, redireciona para a listagem de clientes
    return redirect("/clientes")