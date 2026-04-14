# Importa recursos do Flask:
# Blueprint → permite organizar as rotas em módulos separados (ex: fornecedor, cliente, etc)
# render_template → renderiza arquivos HTML e permite enviar dados para eles
# request → captura dados enviados pelo usuário (formulários HTML)
# redirect → redireciona o usuário para outra rota após alguma ação
from flask import Blueprint, render_template, request, redirect

# Importa funções responsáveis pelas operações no banco (CRUD de fornecedor)
# Essas funções fazem a comunicação direta com o banco de dados
from models.fornecedor.fornecedor_insert import inserir_fornecedor   # CREATE → inserir fornecedor
from models.fornecedor.fornecedor_select import listar_fornecedores  # READ → listar fornecedores
from models.fornecedor.fornecedor_update import atualizar_fornecedor # UPDATE → atualizar fornecedor
from models.fornecedor.fornecedor_delete import excluir_fornecedor   # DELETE → remover fornecedor

# Cria um Blueprint chamado "fornecedor"
# Isso ajuda a organizar o sistema em partes separadas
# "fornecedor" → nome interno usado pelo Flask (ex: url_for)
# __name__ → referência do arquivo atual (necessário para o Flask localizar recursos)
fornecedor_bp = Blueprint("fornecedor", __name__)


# =========================
# TELA DE CADASTRO
# =========================
@fornecedor_bp.route("/fornecedores")  # Define a URL /fornecedores
def fornecedores():
    # Renderiza a página HTML de cadastro de fornecedor
    # Essa página geralmente contém um formulário para inserir dados
    return render_template("fornecedor/fornecedores.html")


# =========================
# INSERIR FORNECEDOR
# =========================
@fornecedor_bp.route("/add_fornecedor", methods=["POST"])  # Rota que recebe dados via POST
def add_fornecedor():
    
    # Chama a função que insere o fornecedor no banco de dados
    # request.form['campo'] → acessa o valor de um input com name="campo"
    # Todos esses dados vêm do formulário HTML enviado pelo usuário
    inserir_fornecedor(
        request.form['nome_empresa'],       # Nome da empresa fornecedora
        request.form['cnpj'],               # CNPJ da empresa (identificador único)
        request.form['produto_quantidade'], # Quantidade de produtos fornecidos
        request.form['preco'],              # Preço unitário do produto
        request.form['rua'],                # Endereço → rua
        request.form['bairro'],             # Endereço → bairro
        request.form['numero'],             # Endereço → número
        request.form['cidade'],             # Endereço → cidade
        request.form['complemento']         # Endereço → complemento (opcional)
    )

    # Após inserir no banco, redireciona para a página de listagem
    # Isso evita reenvio do formulário ao atualizar a página (boa prática)
    return redirect("/lista_fornecedores")


# =========================
# LISTAR FORNECEDORES
# =========================
@fornecedor_bp.route("/lista_fornecedores")  # Rota de listagem
def lista_fornecedores():
    
    # Renderiza o HTML de listagem
    # listar_fornecedores() busca todos os registros no banco
    # Esses dados são enviados para o template na variável "fornecedores"
    return render_template(
        "fornecedor/lista_fornecedores.html",
        fornecedores=listar_fornecedores()
    )


# =========================
# EXCLUIR FORNECEDOR
# =========================
@fornecedor_bp.route("/excluir_fornecedor/<int:id>")  # Recebe o ID pela URL
def excluir_fornecedor_route(id):
    
    # O ID vem da URL (ex: /excluir_fornecedor/3 → id = 3)
    
    # Chama a função que remove o fornecedor do banco
    excluir_fornecedor(id)
    
    # Após excluir, redireciona para a listagem atualizada
    return redirect("/lista_fornecedores")


# =========================
# EDITAR FORNECEDOR
# =========================
@fornecedor_bp.route("/editar_fornecedor/<int:id>")  # Rota para abrir tela de edição
def editar_fornecedor(id):
    
    # Busca o fornecedor dentro da lista pelo ID
    # listar_fornecedores() retorna todos os fornecedores
    # next(...) percorre a lista e retorna o primeiro que satisfaz a condição
    # (f["id"] == id)
    # Se nenhum for encontrado, retorna None (evita erro)
    fornecedor = next((f for f in listar_fornecedores() if f["id"] == id), None)
    
    # Renderiza a página de edição
    # O objeto fornecedor é enviado para o HTML para preencher os campos automaticamente
    return render_template(
        "fornecedor/editar_fornecedor.html",
        fornecedor=fornecedor
    )


# =========================
# ATUALIZAR FORNECEDOR
# =========================
@fornecedor_bp.route("/atualizar_fornecedor/<int:id>", methods=["POST"])  # Recebe dados via POST
def atualizar_fornecedor_route(id):
    
    # Chama a função que atualiza os dados no banco
    # Recebe o ID pela URL e os novos dados pelo formulário
    atualizar_fornecedor(
        id,                                   # ID do fornecedor a ser atualizado
        request.form["nome_empresa"],         # Novo nome da empresa
        request.form["cnpj"],                 # Novo CNPJ
        request.form["produto_quantidade"],   # Nova quantidade de produtos
        request.form["preco"],                # Novo preço
        request.form["rua"],                 # Atualização do endereço
        request.form["bairro"],
        request.form["numero"],
        request.form["cidade"],
        request.form["complemento"]
    )

    # Após atualizar, redireciona para a listagem
    return redirect("/lista_fornecedores")