from flask import Flask, render_template, redirect, url_for, session
# Importa a classe principal Flask e funções auxiliares:
# - render_template: renderiza páginas HTML
# - redirect: redireciona para outra rota
# - url_for: gera URLs dinamicamente
# - session: gerencia sessão do usuário (login)

import os
# Biblioteca padrão do Python usada aqui para gerar chave secreta

from routes.auth_routes import auth_bp
# Importa o blueprint de autenticação (login, logout, registro)

# Importando blueprints de cada módulo (entidade)
from routes.cliente_routes import cliente_bp
from routes.fornecedor_routes import fornecedor_bp
from routes.vendedor_routes import vendedor_bp
from routes.estoque_routes import estoque_bp
from routes.vendas_routes import vendas_bp
from routes.adm_routes import adm_bp
# Importa todos os módulos do sistema organizados em blueprints
# Cada blueprint representa uma parte do sistema (cliente, vendas etc.)

#  Criando a aplicação Flask
app = Flask(__name__)
# Cria a aplicação principal Flask

app.secret_key = os.urandom(24).hex()
# Define uma chave secreta para sessões
# - usada para criptografar cookies de sessão
# - os.urandom(24) gera bytes aleatórios
# - .hex() transforma em string hexadecimal

#  Rota da página inicial
@app.route("/")
def index():
    # Define a rota principal "/"

    # Se não estiver logado, manda para login
    if 'user_id' not in session:
        # Verifica se existe usuário logado na sessão

        return redirect(url_for('auth.login'))
        # Se não estiver logado, redireciona para página de login

    # Logado → renderiza home
    return render_template("index.html")
    # Se estiver logado, mostra a página inicial do sistema


#  Registrando os blueprints sem url_prefix (se não quebra o código)
app.register_blueprint(cliente_bp)
# Registra rotas de cliente no app principal

app.register_blueprint(fornecedor_bp)
# Registra rotas de fornecedor

app.register_blueprint(vendedor_bp)
# Registra rotas de vendedor

app.register_blueprint(estoque_bp)
# Registra rotas de estoque

app.register_blueprint(vendas_bp)
# Registra rotas de vendas

app.register_blueprint(adm_bp)
# Registra rotas de administradores

app.register_blueprint(auth_bp)
# Registra rotas de autenticação (login/logout)

#  Inicializa a aplicação
if __name__ == "__main__":
    # Garante que o servidor só rode se esse arquivo for executado diretamente

    app.run(debug=True)
    # Inicia o servidor Flask em modo debug (mostra erros e recarrega automático)