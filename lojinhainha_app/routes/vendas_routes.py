# Importa recursos do Flask:
# Blueprint → organização de rotas
# render_template → renderizar HTML
# request → pegar dados do formulário
# redirect → redirecionar após ações
from flask import Blueprint, render_template, request, redirect

# Importa funções do model relacionadas a vendas (CRUD)
from models.vendas.vendas_insert import inserir_venda
from models.vendas.vendas_select import listar_vendas
from models.vendas.vendas_update import atualizar_venda
from models.vendas.vendas_delete import excluir_venda

# Importa funções de outras tabelas para relacionamento
from models.cliente.cliente_select import listar_clientes
from models.vendedor.vendedor_select import listar_vendedores
from models.fornecedor.fornecedor_select import listar_fornecedores  

# Cria o blueprint "vendas" para organizar as rotas desse módulo
vendas_bp = Blueprint("vendas", __name__)

# Tela cadastro de vendas
@vendas_bp.route("/vendas")  # Define a URL /vendas
def vendas():
    # Renderiza a página de cadastro de vendas
    # Envia listas de clientes, vendedores e fornecedores para o HTML
    return render_template(
        "vendas/vendas.html",
        clientes=listar_clientes(),       # usado em select de clientes
        vendedores=listar_vendedores(),   # usado em select de vendedores
        fornecedores=listar_fornecedores()  # usado para escolher fornecedor
    )

# NOVA ROTA (usada para pegar o preço do fornecedor dinamicamente)
@vendas_bp.route("/get_preco_fornecedor/<int:id>")
def get_preco_fornecedor(id):
    # Busca todos os fornecedores
    fornecedores = listar_fornecedores()
    
    # Procura o fornecedor com o ID informado
    fornecedor = next((f for f in fornecedores if f["id"] == id), None)

    # Se encontrou o fornecedor
    if fornecedor:
        # Retorna o preço convertido para float (JSON automático)
        return {"preco": float(fornecedor["preco"])}

    # Caso não encontre, retorna preço 0
    return {"preco": 0}

# Inserir venda
@vendas_bp.route("/add_venda", methods=["POST"])  # Recebe dados via POST
def add_venda():
    
    # Converte quantidade para inteiro
    quantidade = int(request.form["quantidade_vendas"])
    
    # Converte fornecedor_id para inteiro
    fornecedor_id = int(request.form["fornecedor_id"])

    # BUSCAR PREÇO REAL DO BANCO (evita manipulação no front-end)
    fornecedores = listar_fornecedores()
    
    # Procura o fornecedor correspondente
    fornecedor = next((f for f in fornecedores if f["id"] == fornecedor_id), None)

    # Se encontrar, pega o preço, senão define como 0
    preco_fornecedor = float(fornecedor["preco"]) if fornecedor else 0

    # CALCULAR NO BACK-END (mais seguro que calcular no front)
    preco_unitario = preco_fornecedor * 1.2  # adiciona margem de lucro (20%)
    preco_total = preco_unitario * quantidade  # calcula total da venda

    # Insere a venda no banco
    inserir_venda(
        request.form["cliente_id"],   # ID do cliente
        request.form["vendedor_id"],  # ID do vendedor
        quantidade,                  # quantidade convertida
        request.form["cpf"],         # CPF do cliente
        preco_unitario,              # preço calculado no backend
        request.form["data"],        # data da venda
        preco_total                 # valor total calculado
    )

    # Redireciona para listagem de vendas
    return redirect("/lista_vendas")

# Listar vendas
@vendas_bp.route("/lista_vendas")
def lista_vendas_route():
    # Renderiza a página com todas as vendas
    return render_template("vendas/lista_vendas.html", vendas=listar_vendas())

# Excluir venda
@vendas_bp.route("/excluir_venda/<int:id>")  # Recebe ID pela URL
def excluir_venda_route(id):
    # Remove a venda do banco
    excluir_venda(id)
    
    # Redireciona para listagem
    return redirect("/lista_vendas")

# Editar venda
@vendas_bp.route("/editar_venda/<int:id>")
def editar_venda(id):
    
    # Busca a venda na lista pelo ID
    venda = next((v for v in listar_vendas() if v["id"] == id), None)
    
    # Renderiza a tela de edição com:
    # - dados da venda
    # - listas de clientes, vendedores e fornecedores
    return render_template(
        "vendas/editar_venda.html",
        venda=venda,
        clientes=listar_clientes(),
        vendedores=listar_vendedores(),
        fornecedores=listar_fornecedores()
    )

# Atualizar venda
@vendas_bp.route("/atualizar_venda/<int:id>", methods=["POST"])
def atualizar_venda_route(id):
    
    # Chama função que atualiza a venda no banco
    atualizar_venda(
        id,
        request.form["cliente_id"],        # novo cliente
        request.form["vendedor_id"],       # novo vendedor
        request.form["quantidade_vendas"], # nova quantidade
        request.form["preco"]              # preço enviado (ou recalculado no model)
    )
    
    # Redireciona para listagem
    return redirect("/lista_vendas")

# Autocomplete clientes (usado para busca dinâmica no front-end)
@vendas_bp.route("/clientes_autocomplete")
def clientes_autocomplete():
    
    # Pega o texto digitado pelo usuário (query string)
    query = request.args.get("q", "")
    
    # Busca todos os clientes
    clientes = listar_clientes()

    # Filtra os clientes cujo nome contém o texto digitado
    resultados = [
        {"id": c["id"], "nome": c["nome"], "cpf": c["cpf"]}
        for c in clientes
        if query.lower() in c["nome"].lower()
    ]
    
    # Retorna os resultados (JSON automático)
    return resultados