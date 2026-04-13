# Importa recursos do Flask:
# Blueprint → organizar rotas
# render_template → renderizar páginas HTML
# request → acessar dados enviados pelo formulário
# redirect → redirecionar o usuário após ações
from flask import Blueprint, render_template, request, redirect

# Importa funções responsáveis pelas operações no banco (CRUD de fornecedor)
from models.fornecedor.fornecedor_insert import inserir_fornecedor
from models.fornecedor.fornecedor_select import listar_fornecedores
from models.fornecedor.fornecedor_update import atualizar_fornecedor
from models.fornecedor.fornecedor_delete import excluir_fornecedor

# Cria um Blueprint chamado "fornecedor"
# Isso ajuda a organizar as rotas separando por módulo
fornecedor_bp = Blueprint("fornecedor", __name__)

# Tela cadastro fornecedor
@fornecedor_bp.route("/fornecedores")  # Define a URL /fornecedores
def fornecedores():
    # Renderiza a página HTML de cadastro de fornecedor
    return render_template("fornecedor/fornecedores.html")

# Inserir fornecedor
@fornecedor_bp.route("/add_fornecedor", methods=["POST"])  # Rota que recebe dados via POST
def add_fornecedor():
    # Chama a função que insere o fornecedor no banco de dados
    # Os dados são capturados do formulário HTML via request.form
    inserir_fornecedor(
        request.form['nome_empresa'],      # Nome da empresa fornecedora
        request.form['cnpj'],              # CNPJ da empresa
        request.form['produto_quantidade'],# Quantidade de produtos fornecidos
        request.form['preco'],             # Preço unitário do produto
        request.form['rua'],               # Dados do endereço
        request.form['bairro'],
        request.form['numero'],
        request.form['cidade'],
        request.form['complemento']
    )
    # Após inserir, redireciona para a página de listagem de fornecedores
    return redirect("/lista_fornecedores")

# Listar fornecedores
@fornecedor_bp.route("/lista_fornecedores")  # Rota de listagem
def lista_fornecedores():
    # Renderiza o HTML passando a lista de fornecedores
    # listar_fornecedores() busca os dados no banco
    return render_template("fornecedor/lista_fornecedores.html",
                           fornecedores=listar_fornecedores())

# Excluir fornecedor
@fornecedor_bp.route("/excluir_fornecedor/<int:id>")  # Recebe o ID pela URL
def excluir_fornecedor_route(id):
    # Chama a função que remove o fornecedor do banco
    excluir_fornecedor(id)
    # Redireciona para a listagem atualizada
    return redirect("/lista_fornecedores")

# Editar fornecedor
@fornecedor_bp.route("/editar_fornecedor/<int:id>")  # Rota para abrir edição
def editar_fornecedor(id):
    # Busca o fornecedor dentro da lista pelo ID
    # next() percorre a lista e retorna o primeiro que bater com o ID
    # Se não encontrar, retorna None
    fornecedor = next((f for f in listar_fornecedores() if f["id"] == id), None)
    
    # Renderiza a página de edição com os dados preenchidos
    return render_template("fornecedor/editar_fornecedor.html", fornecedor=fornecedor)

# Atualizar fornecedor
@fornecedor_bp.route("/atualizar_fornecedor/<int:id>", methods=["POST"])  # Recebe dados via POST
def atualizar_fornecedor_route(id):
    # Chama a função que atualiza os dados no banco
    atualizar_fornecedor(
        id,
        request.form["nome_empresa"],      # Novo nome da empresa
        request.form["cnpj"],              # Novo CNPJ
        request.form["produto_quantidade"],# Nova quantidade
        request.form["preco"],             # Novo preço
        request.form["rua"],               # Atualização do endereço
        request.form["bairro"],
        request.form["numero"],
        request.form["cidade"],
        request.form["complemento"]
    )
    # Redireciona para a listagem após atualizar
    return redirect("/lista_fornecedores")