# Importa recursos do Flask:
# Blueprint → permite organizar rotas em módulos separados (ex: vendas, clientes, etc)
# render_template → renderiza páginas HTML e envia dados para elas
# request → captura dados enviados pelo usuário (formulários ou query string)
# redirect → redireciona o usuário para outra rota após ações
from flask import Blueprint, render_template, request, redirect

# Importa funções do model relacionadas a vendas (CRUD)
# Essas funções fazem comunicação direta com o banco de dados
from models.vendas.vendas_insert import inserir_venda      # CREATE → inserir venda
from models.vendas.vendas_select import listar_vendas      # READ → listar vendas
from models.vendas.vendas_update import atualizar_venda    # UPDATE → atualizar venda
from models.vendas.vendas_delete import excluir_venda      # DELETE → excluir venda

# Importa funções de outras tabelas para relacionamento
# Essas listas são usadas para preencher selects (dropdowns) no HTML
from models.cliente.cliente_select import listar_clientes
from models.vendedor.vendedor_select import listar_vendedores
from models.fornecedor.fornecedor_select import listar_fornecedores  

# Cria o blueprint "vendas" para organizar as rotas desse módulo
# "vendas" → nome interno usado no Flask
# __name__ → referência do arquivo atual
vendas_bp = Blueprint("vendas", __name__)


# =========================
# TELA DE CADASTRO DE VENDAS
# =========================
@vendas_bp.route("/vendas")  # Define a URL /vendas
def vendas():
    
    # Renderiza a página de cadastro de vendas
    # Envia listas para o HTML para popular <select> (dropdowns)
    return render_template(
        "vendas/vendas.html",
        clientes=listar_clientes(),       # lista de clientes (select cliente)
        vendedores=listar_vendedores(),   # lista de vendedores (select vendedor)
        fornecedores=listar_fornecedores()  # lista de fornecedores (usado para preço)
    )


# =========================
# ROTA PARA PEGAR PREÇO DO FORNECEDOR (AJAX)
# =========================
@vendas_bp.route("/get_preco_fornecedor/<int:id>")
def get_preco_fornecedor(id):
    
    # Busca todos os fornecedores do banco
    fornecedores = listar_fornecedores()
    
    # Procura o fornecedor com o ID informado
    # next(...) percorre a lista e retorna o primeiro que bater com a condição
    # Se não encontrar, retorna None
    fornecedor = next((f for f in fornecedores if f["id"] == id), None)

    # Se encontrou o fornecedor
    if fornecedor:
        # Retorna o preço convertido para float
        # Flask automaticamente transforma dicionário em JSON
        return {"preco": float(fornecedor["preco"])}

    # Caso não encontre, retorna preço 0 (evita erro no front)
    return {"preco": 0}


# =========================
# INSERIR VENDA
# =========================
@vendas_bp.route("/add_venda", methods=["POST"])  # Recebe dados via POST
def add_venda():
    
    # Converte quantidade para inteiro (evita erro de tipo)
    quantidade = int(request.form["quantidade_vendas"])
    
    # Converte fornecedor_id para inteiro
    fornecedor_id = int(request.form["fornecedor_id"])

    # BUSCAR PREÇO REAL DO BANCO
    # Isso evita manipulação no front-end (segurança)
    fornecedores = listar_fornecedores()
    
    # Procura o fornecedor correspondente
    fornecedor = next((f for f in fornecedores if f["id"] == fornecedor_id), None)

    # Se encontrar fornecedor, pega o preço
    # Se não, define como 0 para evitar erro
    preco_fornecedor = float(fornecedor["preco"]) if fornecedor else 0

    # CALCULAR NO BACK-END
    # Nunca confiar em valores enviados pelo front-end
    preco_unitario = preco_fornecedor * 1.2  # adiciona 20% de lucro
    preco_total = preco_unitario * quantidade  # total da venda

    # Insere a venda no banco de dados
    inserir_venda(
        request.form["cliente_id"],   # ID do cliente
        request.form["vendedor_id"],  # ID do vendedor
        quantidade,                  # quantidade já convertida
        request.form["cpf"],         # CPF do cliente (pode ser redundante)
        preco_unitario,              # valor calculado no backend
        request.form["data"],        # data da venda
        preco_total                 # valor total calculado
    )

    # Redireciona para a lista de vendas
    return redirect("/lista_vendas")


# =========================
# LISTAR VENDAS
# =========================
@vendas_bp.route("/lista_vendas")
def lista_vendas_route():
    
    # Renderiza a página com todas as vendas
    # listar_vendas() busca dados no banco
    return render_template(
        "vendas/lista_vendas.html",
        vendas=listar_vendas()
    )


# =========================
# EXCLUIR VENDA
# =========================
@vendas_bp.route("/excluir_venda/<int:id>")  # Recebe ID pela URL
def excluir_venda_route(id):
    
    # Remove a venda do banco usando o ID
    excluir_venda(id)
    
    # Redireciona para listagem atualizada
    return redirect("/lista_vendas")


# =========================
# EDITAR VENDA
# =========================
@vendas_bp.route("/editar_venda/<int:id>")
def editar_venda(id):
    
    # Busca a venda dentro da lista pelo ID
    # next(...) percorre até encontrar o item correspondente
    # Se não encontrar, retorna None
    venda = next((v for v in listar_vendas() if v["id"] == id), None)
    
    # Renderiza a tela de edição com:
    # - dados da venda
    # - listas para selects (cliente, vendedor, fornecedor)
    return render_template(
        "vendas/editar_venda.html",
        venda=venda,
        clientes=listar_clientes(),
        vendedores=listar_vendedores(),
        fornecedores=listar_fornecedores()
    )


# =========================
# ATUALIZAR VENDA
# =========================
@vendas_bp.route("/atualizar_venda/<int:id>", methods=["POST"])
def atualizar_venda_route(id):
    
    # Atualiza os dados da venda no banco
    # Recebe o ID pela URL e os novos dados pelo formulário
    atualizar_venda(
        id,
        request.form["cliente_id"],        # novo cliente
        request.form["vendedor_id"],       # novo vendedor
        request.form["quantidade_vendas"], # nova quantidade
        request.form["preco"]              # preço (pode ser recalculado no model)
    )
    
    # Redireciona para listagem
    return redirect("/lista_vendas")


# =========================
# AUTOCOMPLETE DE CLIENTES
# =========================
@vendas_bp.route("/clientes_autocomplete")
def clientes_autocomplete():
    
    # Captura o texto digitado pelo usuário (query string ?q=...)
    query = request.args.get("q", "")
    
    # Busca todos os clientes no banco
    clientes = listar_clientes()

    # Filtra clientes cujo nome contém o texto digitado
    # query.lower() → ignora maiúsculas/minúsculas
    resultados = [
        {
            "id": c["id"], 
            "nome": c["nome"], 
            "cpf": c["cpf"]
        }
        for c in clientes
        if query.lower() in c["nome"].lower()
    ]
    
    # Retorna lista como JSON (Flask converte automaticamente)
    return resultados