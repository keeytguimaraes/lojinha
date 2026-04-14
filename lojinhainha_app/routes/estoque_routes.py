# Importa recursos do Flask
# Blueprint → organiza rotas em módulos separados
# render_template → renderiza HTML
# request → acessa dados enviados pelo formulário
# redirect → redireciona o usuário para outra rota
from flask import Blueprint, render_template, request, redirect

# Importa decorator de autenticação
# Garante que apenas usuários logados acessem certas rotas
from routes.auth_routes import login_required

# Importa funções de CRUD do estoque
# Essas funções fazem comunicação direta com o banco de dados
from models.estoque.estoque_insert import inserir_estoque     # CREATE → inserir item
from models.estoque.estoque_select import listar_estoque      # READ → listar itens
from models.estoque.estoque_update import atualizar_estoque   # UPDATE → atualizar item
from models.estoque.estoque_delete import excluir_estoque     # DELETE → remover item

# Importa função para listar fornecedores
# Necessário para relacionar o estoque com fornecedores (chave estrangeira)
from models.fornecedor.fornecedor_select import listar_fornecedores

# Cria o blueprint para estoque
# "estoque" → nome interno do módulo
# __name__ → referência do arquivo atual
estoque_bp = Blueprint("estoque", __name__)


# =========================
# TELA DE CADASTRO DE ESTOQUE
# =========================
@estoque_bp.route("/estoque")  # rota para acessar a tela de cadastro
@login_required                # exige login
def estoque():
    
    # Renderiza a página de cadastro de estoque
    # Também envia a lista de fornecedores para popular um <select> no HTML
    # Isso permite escolher qual fornecedor está associado ao item
    return render_template(
        "estoque/estoque.html",
        fornecedores=listar_fornecedores()
    )


# =========================
# INSERIR ITEM NO ESTOQUE
# =========================
@estoque_bp.route("/add_estoque", methods=["POST"])
@login_required
def add_estoque():
    
    # Insere um novo item no estoque usando dados do formulário
    # request.form["campo"] → pega valor do input com name="campo"
    inserir_estoque(
        request.form["quantidade_calcas"],  # quantidade de calças no estoque
        request.form["preco_venda"],        # preço de venda do produto
        request.form["fornecedor_id"]       # ID do fornecedor (relacionamento)
    )

    # Após inserir, redireciona para a lista de estoque
    return redirect("/lista_estoque")


# =========================
# LISTAR ESTOQUE
# =========================
@estoque_bp.route("/lista_estoque")
def lista_estoque_route():
    
    # Renderiza a página de listagem de estoque
    # listar_estoque() retorna todos os itens do banco
    # Esses dados são enviados para o HTML na variável "estoque"
    return render_template(
        "estoque/lista_estoque.html",
        estoque=listar_estoque()
    )


# =========================
# EDITAR ITEM DO ESTOQUE
# =========================
@estoque_bp.route("/editar_estoque/<int:id>")
def editar_estoque(id):
    
    # Busca o item específico dentro da lista de estoque
    # listar_estoque() retorna todos os itens
    # next(...) percorre a lista até encontrar o item com o ID correspondente
    # Se não encontrar, retorna None
    item = next((e for e in listar_estoque() if e["id"] == id), None)
    
    # Renderiza a tela de edição
    # Envia:
    # - item → dados do item a ser editado
    # - fornecedores → para permitir alterar o fornecedor no formulário
    return render_template(
        "estoque/editar_estoque.html",
        item=item,
        fornecedores=listar_fornecedores()
    )


# =========================
# ATUALIZAR ESTOQUE
# =========================
@estoque_bp.route("/atualizar_estoque/<int:id>", methods=["POST"])
def atualizar_estoque_route(id):
    
    # Atualiza os dados do item no banco
    # Recebe o ID pela URL e os novos valores pelo formulário
    atualizar_estoque(
        id,                                 # ID do item a ser atualizado
        request.form["quantidade_calcas"],  # nova quantidade
        request.form["preco_venda"],        # novo preço
        request.form["fornecedor_id"]       # novo fornecedor
    )

    # Após atualizar, redireciona para a listagem
    return redirect("/lista_estoque")


# =========================
# EXCLUIR ITEM DO ESTOQUE
# =========================
@estoque_bp.route("/excluir_estoque/<int:id>")
def excluir_estoque_route(id):
    
    # Remove o item do estoque usando o ID recebido na URL
    excluir_estoque(id)
    
    # Redireciona novamente para a listagem
    return redirect("/lista_estoque")