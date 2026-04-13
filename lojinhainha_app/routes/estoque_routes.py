# Importa recursos do Flask
from flask import Blueprint, render_template, request, redirect

# Importa decorator de autenticação
from routes.auth_routes import login_required

# Importa funções de CRUD do estoque
from models.estoque.estoque_insert import inserir_estoque
from models.estoque.estoque_select import listar_estoque
from models.estoque.estoque_update import atualizar_estoque
from models.estoque.estoque_delete import excluir_estoque

# Importa função para listar fornecedores (necessário para relacionamento)
from models.fornecedor.fornecedor_select import listar_fornecedores

# Cria o blueprint para estoque
estoque_bp = Blueprint("estoque", __name__)


# Tela cadastro de estoque
@estoque_bp.route("/estoque")
@login_required
def estoque():
    
    # Renderiza a tela de cadastro de estoque
    # Envia também a lista de fornecedores para o formulário (select)
    return render_template(
        "estoque/estoque.html",
        fornecedores=listar_fornecedores()
    )


# Inserir estoque
@estoque_bp.route("/add_estoque", methods=["POST"])
@login_required
def add_estoque():
    
    # Insere um novo item no estoque com dados do formulário
    inserir_estoque(
        request.form["quantidade_calcas"],
        request.form["preco_venda"],
        request.form["fornecedor_id"]
    )

    # Redireciona para a listagem
    return redirect("/lista_estoque")


# Listar estoque
@estoque_bp.route("/lista_estoque")
def lista_estoque_route():
    
    # Renderiza a lista de itens do estoque
    # Passa os dados retornados do banco
    return render_template(
        "estoque/lista_estoque.html",
        estoque=listar_estoque()
    )


# Editar item do estoque
@estoque_bp.route("/editar_estoque/<int:id>")
def editar_estoque(id):
    
    # Busca o item pelo ID dentro da lista de estoque
    item = next((e for e in listar_estoque() if e["id"] == id), None)
    
    # Renderiza tela de edição
    # Envia também fornecedores para permitir alteração
    return render_template(
        "estoque/editar_estoque.html",
        item=item,
        fornecedores=listar_fornecedores()
    )


# Atualizar estoque
@estoque_bp.route("/atualizar_estoque/<int:id>", methods=["POST"])
def atualizar_estoque_route(id):
    
    # Atualiza os dados do item no banco
    atualizar_estoque(
        id,
        request.form["quantidade_calcas"],
        request.form["preco_venda"],
        request.form["fornecedor_id"]
    )

    # Redireciona para listagem
    return redirect("/lista_estoque")


# Excluir estoque
@estoque_bp.route("/excluir_estoque/<int:id>")
def excluir_estoque_route(id):
    
    # Remove o item do estoque
    excluir_estoque(id)
    
    # Redireciona para listagem
    return redirect("/lista_estoque")