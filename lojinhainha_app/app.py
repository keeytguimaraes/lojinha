# Importa classes e funções principais do Flask
from flask import Flask, render_template, redirect, url_for, session
# - Flask: classe principal para criar a aplicação web
# - render_template: renderiza arquivos HTML da pasta templates
# - redirect: redireciona o usuário para outra rota
# - url_for: gera URLs dinamicamente com base no nome da função/rota
# - session: armazena dados do usuário entre requisições (ex: login)

# Importa o módulo os (biblioteca padrão do Python)
import os
# Usado aqui para gerar uma chave secreta aleatória para segurança da aplicação

# Importa o blueprint responsável pela autenticação
from routes.auth_routes import auth_bp
# Esse módulo normalmente contém rotas de login, logout e registro

# Importando blueprints de cada módulo (organização do sistema)
from routes.cliente_routes import cliente_bp
from routes.fornecedor_routes import fornecedor_bp
from routes.vendedor_routes import vendedor_bp
from routes.estoque_routes import estoque_bp
from routes.vendas_routes import vendas_bp
from routes.adm_routes import adm_bp
# Cada blueprint representa um conjunto de rotas relacionadas a uma entidade
# Exemplo:
# - cliente_bp → rotas de clientes
# - vendas_bp → rotas de vendas
# Isso ajuda a manter o projeto organizado e modular

# Cria a aplicação principal Flask
app = Flask(__name__)
# Aqui o Flask inicia a aplicação web

# Define a chave secreta da aplicação
app.secret_key = os.urandom(24).hex()
# Explicação detalhada:
# - os.urandom(24): gera 24 bytes aleatórios (alta segurança)
# - .hex(): converte esses bytes em uma string hexadecimal
# Essa chave é usada para:
# - Proteger sessões (cookies)
# - Evitar falsificação de dados do usuário

# Define a rota principal do sistema (página inicial)
@app.route("/")
def index():
    # Essa função será executada quando o usuário acessar "/"

    # Verifica se existe um usuário logado na sessão
    # 'user_id' geralmente é definido no login
    if 'user_id' not in session:

        # Se NÃO estiver logado:
        # redireciona para a rota de login do blueprint "auth"
        return redirect(url_for('auth.login'))
        # 'auth.login' → blueprint auth + função login

    # Se estiver logado:
    # renderiza (abre) o arquivo index.html
    return render_template("index.html")

# ===================== BLUEPRINTS =====================
# Blueprint é uma forma de organizar o sistema em módulos separados.
# Cada módulo (cliente, vendas, estoque, etc.) possui suas próprias rotas.
# Isso evita deixar o app.py gigante e facilita manutenção.
# Para ativar um blueprint, usamos: app.register_blueprint()
# Registrando os blueprints na aplicação principal
# Isso "ativa" as rotas de cada módulo dentro do sistema

app.register_blueprint(cliente_bp)
# Agora todas as rotas de cliente estão disponíveis no app

app.register_blueprint(fornecedor_bp)
# Ativa rotas relacionadas a fornecedores

app.register_blueprint(vendedor_bp)
# Ativa rotas de vendedores

app.register_blueprint(estoque_bp)
# Ativa rotas de controle de estoque

app.register_blueprint(vendas_bp)
# Ativa rotas de vendas

app.register_blueprint(adm_bp)
# Ativa rotas administrativas

app.register_blueprint(auth_bp)
# Ativa rotas de autenticação (login, logout, etc.)


# Verifica se este arquivo está sendo executado diretamente
# (e não importado por outro arquivo)
if __name__ == "__main__":

    # Inicia o servidor Flask
    app.run(debug=True)
    # debug=True faz:
    # - Mostra erros detalhados no navegador
    # - Reinicia automaticamente o servidor ao salvar alterações
    # Em produção, isso deve ser False por segurança