from flask import Blueprint, render_template, request, redirect
from models.vendas.vendas_insert import inserir_venda
from models.vendas.vendas_select import listar_vendas
from models.vendas.vendas_update import atualizar_venda
from models.vendas.vendas_delete import excluir_venda
from models.cliente.cliente_select import listar_clientes
from models.vendedor.vendedor_select import listar_vendedores
from models.fornecedor.fornecedor_select import listar_fornecedores  # 🔥 NOVO

vendas_bp = Blueprint("vendas", __name__)

# Tela cadastro de vendas
@vendas_bp.route("/vendas")
def vendas():
    return render_template(
        "vendas/vendas.html",
        clientes=listar_clientes(),
        vendedores=listar_vendedores(),
        fornecedores=listar_fornecedores()  # NOVO
    )

#  NOVA ROTA (igual CPF, mas pro preço)
@vendas_bp.route("/get_preco_fornecedor/<int:id>")
def get_preco_fornecedor(id):
    fornecedores = listar_fornecedores()
    fornecedor = next((f for f in fornecedores if f["id"] == id), None)

    if fornecedor:
        return {"preco": float(fornecedor["preco"])}
    return {"preco": 0}

# Inserir venda
@vendas_bp.route("/add_venda", methods=["POST"])
def add_venda():
    quantidade = int(request.form["quantidade_vendas"])
    fornecedor_id = int(request.form["fornecedor_id"])

    #  BUSCAR PREÇO REAL DO BANCO
    fornecedores = listar_fornecedores()
    fornecedor = next((f for f in fornecedores if f["id"] == fornecedor_id), None)

    preco_fornecedor = float(fornecedor["preco"]) if fornecedor else 0

    #  CALCULAR NO BACK-END (SEGURANÇA)
    preco_unitario = preco_fornecedor * 1.2
    preco_total = preco_unitario * quantidade

    inserir_venda(
        request.form["cliente_id"],
        request.form["vendedor_id"],
        quantidade,
        request.form["cpf"],
        preco_unitario,   # agora vem calculado
        request.form["data"],
        preco_total       #  NOVO
    )

    return redirect("/lista_vendas")

# Listar vendas
@vendas_bp.route("/lista_vendas")
def lista_vendas_route():
    return render_template("vendas/lista_vendas.html", vendas=listar_vendas())

# Excluir venda
@vendas_bp.route("/excluir_venda/<int:id>")
def excluir_venda_route(id):
    excluir_venda(id)
    return redirect("/lista_vendas")

# Editar venda
@vendas_bp.route("/editar_venda/<int:id>")
def editar_venda(id):
    venda = next((v for v in listar_vendas() if v["id"] == id), None)
    return render_template(
        "vendas/editar_venda.html",
        venda=venda,
        clientes=listar_clientes(),
        vendedores=listar_vendedores(),
        fornecedores=listar_fornecedores()  # 🔥 NOVO
    )

# Atualizar venda
@vendas_bp.route("/atualizar_venda/<int:id>", methods=["POST"])
def atualizar_venda_route(id):
    atualizar_venda(
        id,
        request.form["cliente_id"],
        request.form["vendedor_id"],
        request.form["quantidade_vendas"],
        request.form["preco"]
    )
    return redirect("/lista_vendas")

# Autocomplete clientes
@vendas_bp.route("/clientes_autocomplete")
def clientes_autocomplete():
    query = request.args.get("q", "")
    clientes = listar_clientes()

    resultados = [
        {"id": c["id"], "nome": c["nome"], "cpf": c["cpf"]}
        for c in clientes
        if query.lower() in c["nome"].lower()
    ]
    return resultados